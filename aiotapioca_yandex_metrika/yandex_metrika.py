import json
import logging
import random
import re
import time
from aiohttp.client_exceptions import ContentTypeError

from aiotapioca import TapiocaAdapter, JSONAdapterMixin, generate_wrapper_from_adapter
from aiotapioca.exceptions import ResponseProcessException

from . import exceptions
from .resource_mapping import (
    STATS_RESOURCE_MAPPING,
    LOGSAPI_RESOURCE_MAPPING,
    MANAGEMENT_RESOURCE_MAPPING,
)
from .serializers import StatsSerializer, LogsAPISerializer

logger = logging.getLogger(__name__)

LIMIT = 10000


class YandexMetrikaClientAdapterAbstract(JSONAdapterMixin, TapiocaAdapter):
    def get_api_root(self, api_params, resource_name):
        return "https://api-metrika.yandex.net/"

    def get_request_kwargs(self, api_params, *args, **kwargs):
        if "receive_all_data" in api_params:
            raise exceptions.BackwardCompatibilityError("parameter 'receive_all_data'")

        arguments = super().get_request_kwargs(api_params, *args, **kwargs)
        arguments["headers"]["Authorization"] = "OAuth {}".format(
            api_params["access_token"]
        )
        return arguments

    async def get_error_message(self, data, response=None, **kwargs):
        if data is None:
            return {"error_text": await response.text()}
        else:
            return data

    def format_data_to_request(self, data):
        return data

    async def process_response(self, response, **kwargs):
        data = await super().process_response(response, **kwargs)
        if isinstance(data, dict) and "errors" in data:
            raise ResponseProcessException(response, data)
        return data

    def retry_request(
        self,
        tapi_exception,
        error_message,
        repeat_number,
        response,
        request_kwargs,
        api_params,
        **kwargs
    ):
        code = int(error_message.get("code", 0))
        message = error_message.get("message", "")
        errors_types = [i.get("error_type") for i in error_message.get("errors", [])]

        limit_errors = {
            "quota_requests_by_uid": "The limit on the number of API requests per day for the user has been exceeded.",
            "quota_delegate_requests": "Exceeded the limit on the number of API requests to add representatives per hour for a user.",
            "quota_grants_requests": "Exceeded the limit on the number of API requests to add access to the counter per hour",
            "quota_requests_by_ip": "The limit on the number of API requests per second for an IP address has been exceeded.",
            "quota_parallel_requests": "The limit on the number of parallel API requests per day for the user has been exceeded.",
            "quota_requests_by_counter_id": "The limit on the number of API requests per day for the counter has been exceeded.",
        }
        big_report_request = (
            "Query is too complicated. Please reduce the date interval or sampling."
        )

        if code == 400:
            if message == big_report_request:
                if repeat_number < 10:
                    retry_seconds = random.randint(5, 30)
                    big_report_request += " Re-request after {} seconds".format(
                        retry_seconds
                    )
                    logger.warning(big_report_request)
                    time.sleep(retry_seconds)
                    return True

        if code == 429:
            if "quota_requests_by_ip" in errors_types:
                retry_seconds = random.randint(1, 30)
                error_text = "{} Re-request after {} seconds.".format(
                    limit_errors["quota_requests_by_ip"], retry_seconds
                )
                logger.warning(error_text)
                time.sleep(retry_seconds)
                return True
            else:
                for err in errors_types:
                    logger.error(limit_errors[err])

        elif code == 503:
            if repeat_number < api_params.get("retries_if_server_error", 3):
                logger.warning("Server error. Re-request after 3 seconds")
                time.sleep(5)
                return True

        return False

    def error_handling(
        self,
        tapi_exception,
        error_message,
        repeat_number,
        response,
        request_kwargs,
        api_params,
        **kwargs
    ):
        if "error_text" in error_message:
            raise exceptions.YandexMetrikaApiError(
                response, error_message["error_text"]
            )
        else:
            error_code = int(error_message.get("code", 0))

            if error_code == 429:
                raise exceptions.YandexMetrikaLimitError(response, **error_message)
            elif error_code == 403:
                raise exceptions.YandexMetrikaTokenError(response, **error_message)
            else:
                raise exceptions.YandexMetrikaClientError(response, **error_message)


class YandexMetrikaManagementClientAdapter(YandexMetrikaClientAdapterAbstract):
    resource_mapping = MANAGEMENT_RESOURCE_MAPPING


class YandexMetrikaLogsAPIClientAdapter(YandexMetrikaClientAdapterAbstract):
    resource_mapping = LOGSAPI_RESOURCE_MAPPING
    serializer_class = LogsAPISerializer

    async def response_to_native(self, response, **kwargs):
        try:
            return await response.json()
        except ContentTypeError:
            text = await response.text()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
        except json.JSONDecodeError:
            return await response.text()

    def error_handling(
        self,
        tapi_exception,
        error_message,
        repeat_number,
        response,
        request_kwargs,
        api_params,
        **kwargs
    ):
        message = error_message.get("message")
        if message == "Incorrect part number":
            # Fires when trying to download a non-existent part of a report.
            return

        if message == "Only log of requests in status 'processed' can be downloaded":
            raise exceptions.YandexMetrikaDownloadReportError(response)

        return super().error_handling(
            tapi_exception,
            error_message,
            repeat_number,
            response,
            request_kwargs,
            api_params,
            **kwargs
        )

    def _is_exists_report(self, response, api_params, **kwargs):
        request_id = api_params["default_url_params"]["requestId"]
        if kwargs["store"].get(request_id) is None:
            client = kwargs["client"]
            info = client.info(requestId=request_id).get()
            status = info.data["log_request"]["status"]
            if "cleaned" in status:
                raise exceptions.YandexMetrikaDownloadReportError(
                    response,
                    message="The report does not exist, it has been cleared. "
                    "Current report status is '{}'".format(status),
                )
            kwargs["store"][request_id] = "exists"

    def retry_request(
        self,
        tapi_exception,
        error_message,
        repeat_number,
        response,
        request_kwargs,
        api_params,
        **kwargs
    ):
        """
        Conditions for repeating a request. If it returns True, the request will be repeated.
        """
        message = error_message.get("message")

        if (
            message == "Only log of requests in status 'processed' can be downloaded"
            and "download" in request_kwargs["url"]
            and api_params.get("wait_report", False)
        ):
            self._is_exists_report(response, api_params, **kwargs)

            # The error appears when trying to download an unprepared report.
            max_sleep = 60 * 5
            sleep_time = repeat_number * 60
            sleep_time = sleep_time if sleep_time <= max_sleep else max_sleep
            logger.info("Wait report {} sec.".format(sleep_time))
            time.sleep(sleep_time)

            return True

        return super().retry_request(
            tapi_exception,
            error_message,
            repeat_number,
            response,
            request_kwargs,
            api_params,
            **kwargs
        )

    def fill_resource_template_url(self, template, url_params, **kwargs):
        resource = kwargs.get("resource")
        if "download" in resource["resource"] and not url_params.get("partNumber"):
            url_params.update(partNumber=0)
        return super().fill_resource_template_url(template, url_params, **kwargs)

    def get_iterator_next_request_kwargs(
        self, request_kwargs, data, response, **kwargs
    ):
        url = request_kwargs["url"]

        if "download" not in url:
            raise NotImplementedError("Iteration not supported for this resource")

        part = int(re.findall(r"part/([0-9]*)/", url)[0])
        next_part = part + 1
        new_url = re.sub(r"part/[0-9]*/", "part/{}/".format(next_part), url)
        return {**request_kwargs, "url": new_url}

    def get_iterator_list(self, data, **kwargs):
        if data:
            return [data]
        else:
            return []


class YandexMetrikaStatsClientAdapter(YandexMetrikaClientAdapterAbstract):
    resource_mapping = STATS_RESOURCE_MAPPING
    serializer_class = StatsSerializer

    async def process_response(self, response, **kwargs):
        data = await super().process_response(response, **kwargs)
        attribution = data["query"]["attribution"]
        sampled = data["sampled"]
        sample_share = data["sample_share"]
        total_rows = int(data["total_rows"])
        offset = data["query"]["offset"]
        limit = int(response.url.query.get("limit", LIMIT))
        offset2 = offset + limit - 1
        if offset2 > total_rows:
            offset2 = total_rows

        if sampled:
            logger.info("Sample: {}".format(sample_share))
        logger.info("Attribution: {}".format(attribution))
        logger.info(
            "Exported lines {}-{}. Total rows {}".format(offset, offset2, total_rows)
        )

        return data

    def get_iterator_next_request_kwargs(
        self, request_kwargs, data, response, **kwargs
    ):
        total_rows = int(data["total_rows"])
        limit = request_kwargs["params"].get("limit", LIMIT)
        offset = data["query"]["offset"] + limit

        if offset <= total_rows:
            request_kwargs["params"]["offset"] = offset
            return request_kwargs

    def get_iterator_list(self, data, **kwargs):
        return [data]


YandexMetrikaStats = generate_wrapper_from_adapter(YandexMetrikaStatsClientAdapter)
YandexMetrikaLogsAPI = generate_wrapper_from_adapter(YandexMetrikaLogsAPIClientAdapter)
YandexMetrikaManagement = generate_wrapper_from_adapter(
    YandexMetrikaManagementClientAdapter
)
