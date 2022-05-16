import re
import time
from asyncio import run as asyncio_run
from datetime import date
from inspect import isclass
from logging import getLogger
from random import randint

from aiotapioca.adapters import (
    JSONAdapterMixin,
    TapiocaAdapter,
    generate_wrapper_from_adapter,
)
from aiotapioca.exceptions import ResponseProcessException
from orjson import JSONDecodeError, loads

from .exceptions import (
    BackwardCompatibilityError,
    YandexMetrikaApiError,
    YandexMetrikaClientError,
    YandexMetrikaDownloadReportError,
    YandexMetrikaLimitError,
    YandexMetrikaServerError,
    YandexMetrikaTokenError,
)
from .resource_mapping import (
    LOGS_API_RESOURCE_MAPPING,
    MANAGEMENT_API_RESOURCE_MAPPING,
    REPORTS_API_RESOURCE_MAPPING,
)

logger = getLogger(__name__)

LIMIT = 10000


class YandexMetrikaClientAdapterAbstract(JSONAdapterMixin, TapiocaAdapter):
    def get_api_root(self, api_params, **kwargs):
        return "https://api-metrika.yandex.net/"

    def get_request_kwargs(self, *args, **kwargs):
        api_params = kwargs.get("api_params", {})
        if "receive_all_data" in api_params:
            raise BackwardCompatibilityError("parameter 'receive_all_data'")

        arguments = super().get_request_kwargs(*args, **kwargs)
        arguments["headers"]["Authorization"] = "OAuth {}".format(
            api_params["access_token"]
        )
        return arguments

    def get_iterator_list(self, data, **kwargs):
        if data:
            return [data]
        else:
            return []

    async def get_error_message(self, data, response=None, **kwargs):
        if data is None:
            return {"error_text": await response.text()}
        else:
            return data

    async def process_response(self, response, **kwargs):
        data = await self.response_to_native(response, **kwargs)
        if response.status == 403:
            raise ResponseProcessException(YandexMetrikaTokenError, data)
        elif response.status == 429:
            raise ResponseProcessException(YandexMetrikaLimitError, data)
        elif 400 <= response.status < 500:
            raise ResponseProcessException(YandexMetrikaClientError, data)
        elif 500 <= response.status < 600:
            raise ResponseProcessException(YandexMetrikaServerError, data)
        return data

    def retry_request(
        self,
        exception=None,
        error_message=None,
        repeat_number=0,
        **kwargs,
    ):
        api_params = kwargs["api_params"]
        response = kwargs["response"]
        error_message = error_message if error_message else {}

        code = int(error_message.get("code", response.status))
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
                    retry_seconds = randint(5, 30)
                    big_report_request += " Re-request after {} seconds".format(
                        retry_seconds
                    )
                    logger.warning(big_report_request)
                    time.sleep(retry_seconds)
                    return True

        if code == 429:
            if "quota_requests_by_ip" in errors_types:
                retry_seconds = randint(1, 30)
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
        exception=None,
        error_message=None,
        repeat_number=0,
        **kwargs,
    ):
        if isclass(exception) and issubclass(exception, YandexMetrikaApiError):
            response = kwargs["response"]
            if "error_text" in error_message:
                raise YandexMetrikaApiError(response, error_message["error_text"])
            else:
                raise exception(response, **error_message)
        else:
            super().error_handling(exception, error_message, repeat_number, **kwargs)


class YandexMetrikaManagementAPIClientAdapter(YandexMetrikaClientAdapterAbstract):
    resource_mapping = MANAGEMENT_API_RESOURCE_MAPPING

    def get_request_kwargs(self, *args, **kwargs):
        arguments = super().get_request_kwargs(*args, **kwargs)

        if self.resource_mapping["counters"] == kwargs["resource"]:
            params = arguments.get("params", {})
            params.setdefault("per_page", LIMIT)
            arguments["params"] = params

        return arguments

    async def process_response(self, response, **kwargs):
        data = await super().process_response(response, **kwargs)

        if self.resource_mapping["counters"] == kwargs["resource"]:
            total_rows = data["rows"]
            per_page = int(response.url.query.get("per_page", LIMIT))
            offset = int(response.url.query.get("offset", 1)) + per_page
            offset2 = offset + per_page - 1
            if offset2 > total_rows:
                offset2 = total_rows

            logger.debug(
                "Exported lines {}-{}. Total rows {}".format(
                    offset, offset2, total_rows
                )
            )

        return data

    def get_iterator_next_request_kwargs(
        self, request_kwargs, data, response, **kwargs
    ):
        if self.resource_mapping["counters"] == kwargs["resource"]:
            total_rows = data["rows"]
            per_page = int(response.url.query.get("per_page", LIMIT))
            offset = int(response.url.query.get("offset", 1)) + per_page

            if offset <= total_rows:
                request_kwargs["params"]["offset"] = offset
                return request_kwargs


class YandexMetrikaReportsAPIClientAdapter(YandexMetrikaClientAdapterAbstract):
    resource_mapping = REPORTS_API_RESOURCE_MAPPING

    @staticmethod
    def _convert_date_to_str_format(dt):
        if isinstance(dt, date):
            return dt.strftime("%Y-%m-%d")
        elif isinstance(dt, str):
            return dt
        else:
            raise TypeError(
                'Parameters "date1" and "date2" must be of the datetime, date or string type.'
            )

    def get_request_kwargs(self, *args, **kwargs):
        arguments = super().get_request_kwargs(*args, **kwargs)

        params = arguments.get("params", {})
        if params:
            params["date1"] = self._convert_date_to_str_format(params.get("date1"))
            params["date2"] = self._convert_date_to_str_format(params.get("date2"))

        params.setdefault("limit", LIMIT)

        arguments["params"] = params

        return arguments

    async def process_response(self, response, **kwargs):
        data = await super().process_response(response, **kwargs)
        attribution = data["query"]["attribution"]
        sampled = data["sampled"]
        sample_share = data["sample_share"]
        total_rows = data["total_rows"]
        limit = data["query"]["limit"]
        offset = data["query"]["offset"]
        offset2 = offset + limit - 1
        if offset2 > total_rows:
            offset2 = total_rows

        if sampled:
            logger.debug("Sample: {}".format(sample_share))
        logger.debug("Attribution: {}".format(attribution))
        logger.debug(
            "Exported lines {}-{}. Total rows {}".format(offset, offset2, total_rows)
        )

        return data

    def get_iterator_next_request_kwargs(
        self, request_kwargs, data, response, **kwargs
    ):
        total_rows = data["total_rows"]
        limit = int(response.url.query.get("limit", LIMIT))
        offset = int(response.url.query.get("offset", 1)) + limit

        if offset <= total_rows:
            request_kwargs["params"]["offset"] = offset
            return request_kwargs


class YandexMetrikaLogsAPIClientAdapter(YandexMetrikaClientAdapterAbstract):
    resource_mapping = LOGS_API_RESOURCE_MAPPING

    async def response_to_native(self, response, **kwargs):
        text = await response.text()

        if not text:
            return None

        try:
            return loads(text)
        except JSONDecodeError:
            return text

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

    async def _check_status_report(self, response, api_params, **kwargs):
        request_id = api_params["default_url_params"].get("requestId")
        if request_id is None:
            client = kwargs["client"]
            info = await client.info(requestId=request_id).get()
            status = info().data["log_request"]["status"]
            if status not in ("processed", "created"):
                raise YandexMetrikaDownloadReportError(
                    response,
                    message=f"Such status '{status}' of the report does not allow downloading it",
                )

    def retry_request(
        self,
        exception=None,
        error_message=None,
        repeat_number=0,
        **kwargs,
    ):
        """
        Conditions for repeating a request. If it returns True, the request will be repeated.
        """
        response = kwargs["response"]
        request_kwargs = kwargs["request_kwargs"]
        api_params = kwargs["api_params"]
        message = error_message.get("message")

        if (
            message == "Only log of requests in status 'processed' can be downloaded"
            and "download" in request_kwargs["url"]
            and api_params.get("wait_report", False)
        ):
            asyncio_run(self._check_status_report(response, api_params, **kwargs))

            # The error appears when trying to download an unprepared report.
            max_sleep = 60 * 5
            sleep_time = repeat_number * 60
            sleep_time = sleep_time if sleep_time <= max_sleep else max_sleep
            logger.info("Wait report %s sec.", sleep_time)
            time.sleep(sleep_time)

            return True

        return super().retry_request(
            exception,
            error_message,
            repeat_number,
            **kwargs,
        )

    def error_handling(
        self,
        exception=None,
        error_message=None,
        repeat_number=0,
        **kwargs,
    ):
        message = error_message.get("message")
        if message == "Incorrect part number":
            # Fires when trying to download a non-existent part of a report.
            return

        if message == "Only log of requests in status 'processed' can be downloaded":
            raise YandexMetrikaDownloadReportError(kwargs["response"])

        return super().error_handling(
            exception,
            error_message,
            repeat_number,
            **kwargs,
        )


YandexMetrikaReportsAPI = generate_wrapper_from_adapter(
    YandexMetrikaReportsAPIClientAdapter
)
YandexMetrikaManagementAPI = generate_wrapper_from_adapter(
    YandexMetrikaManagementAPIClientAdapter
)
YandexMetrikaLogsAPI = generate_wrapper_from_adapter(YandexMetrikaLogsAPIClientAdapter)
