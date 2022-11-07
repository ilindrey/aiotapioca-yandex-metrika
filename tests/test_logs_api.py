from io import StringIO
from json import dumps

import pytest
import pytest_asyncio
from response_data import LOGS_DATA
from utils import make_url

from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI


@pytest.fixture
def url_params_visits():
    return {
        "fields": ["ym:s:date"],
        "source": "visits",
        "date1": "2020-12-01",
        "date2": "2020-12-02",
    }


@pytest.fixture
def url_params_hits():
    return {
        "fields": ["ym:pv:date"],
        "source": "hits",
        "date1": "2020-12-01",
        "date2": "2020-12-02",
    }


@pytest_asyncio.fixture
async def client():
    default_params = {
        "access_token": "token",
        "default_url_params": {"counter_id": 100500},
        "wait_report": True,
    }
    async with YandexMetrikaLogsAPI(**default_params) as c:
        yield c


async def test_all_info(mocked, client, url_params_visits, url_params_hits):
    response_data = {
        "requests": [
            {
                "request_id": 12345678,
                "counter_id": 100500,
                "source": url_params_visits["source"],
                "date1": url_params_visits["date1"],
                "date2": url_params_visits["date2"],
                "fields": url_params_visits["fields"],
                "status": "processed",
                "size": 15555,
                "parts": [{"part_number": 0, "size": 15555}],
                "attribution": "LASTSIGN",
            },
            {
                "request_id": 87654321,
                "counter_id": 100500,
                "source": url_params_hits["source"],
                "date1": url_params_hits["date1"],
                "date2": url_params_hits["date2"],
                "fields": url_params_hits["fields"],
                "status": "processed",
                "size": 555555,
                "parts": [{"part_number": 0, "size": 555555}],
                "attribution": "LASTSIGN",
            },
        ]
    }

    mocked.get(
        client.all_info().path,
        body=dumps(response_data),
        status=200,
        content_type="application/json",
    )

    response = await client.all_info().get()

    assert response.data() == response_data


async def test_evaluate(mocked, client, url_params_visits):

    response_data = {
        "log_request_evaluation": {
            "possible": True,
            "max_possible_day_quantity": 7777777,
        },
    }

    mocked.get(
        make_url(client.evaluate().path, url_params_visits),
        body=dumps(response_data),
        status=200,
        content_type="application/json",
    )
    response = await client.evaluate().get(params=url_params_visits)

    assert "log_request_evaluation" in response.data
    assert response.data() == response_data
    assert response.data.log_request_evaluation.possible() is True
    assert response.data.log_request_evaluation.max_possible_day_quantity() == 7777777


async def test_create(mocked, client, url_params_visits):
    response_data = {
        "log_request": {
            "request_id": 12345678,
            "counter_id": 100500,
            "source": url_params_visits["source"],
            "date1": url_params_visits["date1"],
            "date2": url_params_visits["date2"],
            "fields": url_params_visits["fields"],
            "status": "created",
            "attribution": "LASTSIGN",
        }
    }
    mocked.post(
        make_url(client.create().path, url_params_visits),
        body=dumps(response_data),
        status=200,
        content_type="application/json",
    )
    response = await client.create().post(params=url_params_visits)

    assert "log_request" in response.data
    assert response.data.log_request.status() == "created"
    assert response.data.log_request.date1() == url_params_visits["date1"]
    assert response.data.log_request.date2() == url_params_visits["date2"]
    assert response.data() == response_data


async def test_info(mocked, client, url_params_visits):
    response_data = {
        "log_request": {
            "request_id": 12345678,
            "counter_id": 100500,
            "source": url_params_visits["source"],
            "date1": url_params_visits["date1"],
            "date2": url_params_visits["date2"],
            "fields": url_params_visits["fields"],
            "status": "processed",
            "size": 15555,
            "parts": [{"part_number": 1, "size": 15555}],
            "attribution": "LASTSIGN",
        }
    }
    mocked.get(
        client.info(request_id=12345678).path,
        body=dumps(response_data),
        status=200,
        content_type="application/json",
    )
    response = await client.info(request_id=12345678).get()

    assert "log_request" in response.data
    assert response.data.log_request.counter_id() == 100500
    assert response.data.log_request.request_id() == 12345678


async def test_download(mocked, client):
    counter_id = 100500
    request_id = 12345678

    url_1 = (
        "https://api-metrika.yandex.net/management/v1/counter/"
        f"{counter_id}/logrequest/{request_id}/part/0/download"
    )
    url_2 = (
        "https://api-metrika.yandex.net/management/v1/counter/"
        f"{counter_id}/logrequest/{request_id}/part/1/download"
    )

    mocked.get(url_1, body=LOGS_DATA, status=200)
    mocked.get(url_2, body=LOGS_DATA, status=200)

    log = await client.download(request_id=12345678).get()
    async for page in log().pages(max_pages=2):
        assert page.data() == LOGS_DATA


async def test_clean(mocked, client, url_params_visits):
    response_data = {
        "log_request": {
            "request_id": 12345678,
            "counter_id": 100500,
            "source": url_params_visits["source"],
            "date1": url_params_visits["date1"],
            "date2": url_params_visits["date2"],
            "fields": url_params_visits["fields"],
            "status": "cleaned_by_user",
            "size": 2382,
            "parts": [{"part_number": 0, "size": 2382}],
            "attribution": "LASTSIGN",
        }
    }
    mocked.post(
        client.clean(request_id=12345678).path,
        body=dumps(response_data),
        status=200,
        content_type="application/json",
    )

    response = await client.clean(request_id=12345678).post()

    assert "log_request" in response.data
    assert response.data.log_request.counter_id() == 100500
    assert response.data.log_request.request_id() == 12345678
    assert response.data.log_request.status() == "cleaned_by_user"


async def test_cancel(mocked, client, url_params_visits):
    response_data = {
        "log_request": {
            "request_id": 12345678,
            "counter_id": 100500,
            "source": url_params_visits["source"],
            "date1": url_params_visits["date1"],
            "date2": url_params_visits["date2"],
            "fields": url_params_visits["fields"],
            "status": "canceled",
            "size": 0,
            "attribution": "LASTSIGN",
        }
    }
    mocked.post(
        client.cancel(request_id=12345678).path,
        body=dumps(response_data),
        status=200,
        content_type="application/json",
    )

    response = await client.cancel(request_id=12345678).post()

    assert "log_request" in response.data
    assert response.data.log_request.counter_id() == 100500
    assert response.data.log_request.request_id() == 12345678
    assert response.data.log_request.status() == "canceled"


async def test_transform(mocked, client):
    mocked.get(
        "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/0/part/0/download",
        body=LOGS_DATA,
        status=200,
        content_type="application/json",
    )

    log = await client.download(request_id=0).get()

    assert log.data.headers() == ["col1", "col2", "col3", "col4", "col5"]

    assert log.data.values() == [
        ["val1", "val2", "val3", "val4", "val5"],
        ["val11", "val22", "val33", "val44", "val55"],
        ["val111", "val222", "val333", "val444", "val555"],
        ["val1111", "val2222", "val3333", "val4444", "val5555"],
    ]
    assert log.data.lines() == [
        "val1\tval2\tval3\tval4\tval5",
        "val11\tval22\tval33\tval44\tval55",
        "val111\tval222\tval333\tval444\tval555",
        "val1111\tval2222\tval3333\tval4444\tval5555",
    ]
    assert log.data.columns() == [
        ["val1", "val11", "val111", "val1111"],
        ["val2", "val22", "val222", "val2222"],
        ["val3", "val33", "val333", "val3333"],
        ["val4", "val44", "val444", "val4444"],
        ["val5", "val55", "val555", "val5555"],
    ]
    assert log.data.dicts() == [
        {
            "col1": "val1",
            "col2": "val2",
            "col3": "val3",
            "col4": "val4",
            "col5": "val5",
        },
        {
            "col1": "val11",
            "col2": "val22",
            "col3": "val33",
            "col4": "val44",
            "col5": "val55",
        },
        {
            "col1": "val111",
            "col2": "val222",
            "col3": "val333",
            "col4": "val444",
            "col5": "val555",
        },
        {
            "col1": "val1111",
            "col2": "val2222",
            "col3": "val3333",
            "col4": "val4444",
            "col5": "val5555",
        },
    ]


async def test_iteration(mocked, client):

    columns = LOGS_DATA.split("\n")[0].split("\t")

    def _iter_line(text):
        lines = StringIO(text)
        next(lines)  # skipping columns
        return (line.replace("\n", "") for line in lines)

    def to_columns(data):
        cols = [[] for _ in range(len(columns))]
        for line in _iter_line(data):
            values = line.split("\t")
            for i, col in enumerate(cols):
                col.append(values[i])
        return cols

    expected_lines = LOGS_DATA.split("\n")[1:]
    expected_values = [i.split("\t") for i in LOGS_DATA.split("\n")[1:]]
    expected_columns = to_columns(LOGS_DATA)
    expected_dicts = [dict(zip(columns, i.split("\t"))) for i in LOGS_DATA.split("\n")[1:]]

    url_1 = (
        "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/0/part/0/download"
    )
    url_2 = (
        "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/0/part/1/download"
    )

    mocked.get(url_1, body=LOGS_DATA, status=200)
    mocked.get(url_2, body=LOGS_DATA, status=200)

    log = await client.download(request_id=0).get()

    max_parts = 2
    async for part in log().pages(max_pages=max_parts):
        assert len(part.data.lines()) == 4
        assert len(part.data.values()) == 4
        assert len(part.data.columns()) == 5
        assert len(part.data.dicts()) == 4

        assert part.data.headers() == ["col1", "col2", "col3", "col4", "col5"]

        for line, expected in zip(part.data.lines(), expected_lines):
            assert line == expected

        for values, expected in zip(part.data.values(), expected_values):
            assert values == expected

        for values, expected in zip(part.data.columns(), expected_columns):
            assert values == expected

        for values, expected in zip(part.data.dicts(), expected_dicts):
            assert values == expected
