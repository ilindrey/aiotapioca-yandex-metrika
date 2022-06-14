import pytest
import pytest_asyncio
from orjson import dumps
from response_data import COUNTERS_DATA

from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI, YandexMetrikaManagementAPI
from aiotapioca_yandex_metrika.aiotapioca_yandex_metrika import LIMIT
from aiotapioca_yandex_metrika.exceptions import (
    BackwardCompatibilityError,
    YandexMetrikaApiError,
    YandexMetrikaClientError,
    YandexMetrikaDownloadLogError,
    YandexMetrikaLimitError,
    YandexMetrikaServerError,
    YandexMetrikaTokenError,
)


@pytest_asyncio.fixture
async def client():
    async with YandexMetrikaManagementAPI(access_token="token") as c:
        yield c


def get_response_body(code, error_type, message=None, errors=None):
    errors = errors or [{"error_type": error_type, "message": message}]
    message = message or "some message"
    response_body = {"errors": errors, "code": code, "message": message}
    return response_body, message, errors


async def test_adapter_raises_response_process_exception_on_403s(mocked, client):
    code = 403
    error_type = "access_denied"

    response_body, message, errors = get_response_body(code, error_type)

    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body=dumps(response_body),
        status=code,
        content_type="application/json",
    )
    with pytest.raises(YandexMetrikaTokenError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"


async def test_adapter_raises_response_process_exception_on_429s(mocked, client):

    retry_count = client._api.max_retries_requests + 1

    code = 429

    error_type = "quota_requests_by_uid"
    response_body, message, errors = get_response_body(code, error_type)

    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body=dumps(response_body),
        status=code,
        content_type="application/json",
    )
    with pytest.raises(YandexMetrikaLimitError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"

    error_type = "quota_requests_by_ip"
    response_body, message, errors = get_response_body(code, error_type)

    for _ in range(retry_count):
        mocked.get(
            client.counters().path + f"?per_page={LIMIT}",
            body=dumps(response_body),
            status=code,
            content_type="application/json",
        )
    with pytest.raises(YandexMetrikaLimitError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"


async def test_adapter_raises_response_process_exception_on_400s(mocked, client):

    retry_count = client._api.max_retries_requests + 1

    code = 400

    error_type = "invalid_parameter"
    response_body, message, errors = get_response_body(code, error_type)

    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body=dumps(response_body),
        status=code,
        content_type="application/json",
    )
    with pytest.raises(YandexMetrikaClientError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"

    code = 400

    error_type = "invalid_parameter"
    message = "Query is too complicated. Please reduce the date interval or sampling."
    response_body, message, errors = get_response_body(code, error_type, message)

    for _ in range(retry_count):
        mocked.get(
            client.counters().path + f"?per_page={LIMIT}",
            body=dumps(response_body),
            status=code,
            content_type="application/json",
        )
    with pytest.raises(YandexMetrikaClientError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"


async def test_adapter_raises_response_process_exception_on_503s(mocked, client):

    retry_count = client._api.max_retries_requests + 1

    code = 503

    error_type = "backend_error"
    response_body, message, errors = get_response_body(code, error_type)

    for _ in range(retry_count):
        mocked.get(
            client.counters().path + f"?per_page={LIMIT}",
            body=dumps(response_body),
            status=code,
            content_type="application/json",
        )
    with pytest.raises(YandexMetrikaServerError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"


async def test_adapter_raises_response_process_exception_on_504s(mocked, client):

    code = 504

    error_type = "timeout"
    response_body, message, errors = get_response_body(code, error_type)

    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body=dumps(response_body),
        status=code,
        content_type="application/json",
    )
    with pytest.raises(YandexMetrikaServerError) as ex:
        await client.counters().get()
    assert str(ex.value) == f"code={code}, message={message}, errors={errors}"


async def test_adapter_raises_response_process_common_exception(mocked, client):

    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body="{}",
        status=504,
        content_type="application/json",
    )
    with pytest.raises(YandexMetrikaApiError):
        await client.counters().get()


async def test_adapter_raises_response_process_backward_compatibility_exception(mocked):

    client = YandexMetrikaManagementAPI(receive_all_data=True)

    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body=COUNTERS_DATA,
        status=200,
        content_type="application/json",
    )

    with pytest.raises(BackwardCompatibilityError):
        await client.counters().get()


async def test_adapter_raises_response_process_download_log_error(mocked):

    default_params = dict(
        access_token="token",
        default_url_params={"counterId": 100500},
        wait_report=True,
    )
    client = YandexMetrikaLogsAPI(**default_params)

    retry_count = client._api.max_retries_requests + 1

    requestId = 12345678
    code = 400
    error_type = "invalid_parameter"
    url = "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/12345678/part/0/download"
    message = f"Only log of requests in status 'processed' can be downloaded"

    response_body, message, errors = get_response_body(code, error_type, message)

    mocked.get(
        url,
        body=dumps(response_body),
        status=code,
        content_type="application/json",
    )

    with pytest.raises(YandexMetrikaDownloadLogError):
        await client.download(requestId=requestId).get()

    mocked.get(
        url,
        body=dumps(response_body),
        status=code,
        content_type="application/json",
    )

    for _ in range(retry_count):
        mocked.get(
            client.info(requestId=requestId).path,
            body=dumps(response_body),
            status=200,
            content_type="application/json",
        )

    with pytest.raises(YandexMetrikaDownloadLogError):
        await client.download(requestId=requestId).get()
