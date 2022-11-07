from datetime import date
from json import loads

import pytest_asyncio
from response_data import REPORTS_DATA
from utils import make_url

from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI


url_params = {
    "ids": 100500,
    "metrics": "ym:s:visits",
    "dimensions": "ym:s:date",
    "sort": "ym:s:date",
    "filters": "ym:s:startURL=.('https://rfgf.ru/map','https://rfgf.ru/map')",
    "group": "Day",
    "date1": date(2022, 10, 1),
    "date2": date(2022, 10, 5),
    "limit": 1,
}


@pytest_asyncio.fixture
async def client():
    async with YandexMetrikaReportsAPI(access_token="token") as c:
        yield c


async def test_reports_data(mocked, client):
    mocked.get(
        make_url(client.reports().path, url_params),
        body=REPORTS_DATA,
        status=200,
        content_type="application/json",
    )

    response = await client.reports().get(params=url_params)

    assert response.data() == loads(REPORTS_DATA)
    assert response.data.query.ids() == [100500]
    assert response.data.query.limit() == 1
    assert len(response.data.data()) > 0
    assert len(response.data.totals()) > 0
    assert response.data.totals()[0] > 0


async def test_transform(mocked, client):
    mocked.get(
        make_url(client.reports().path, url_params),
        body=REPORTS_DATA,
        status=200,
        content_type="application/json",
    )

    response = await client.reports().get(params=url_params)

    response_data = loads(REPORTS_DATA)

    assert response.data() == response_data
    assert response.data.headers() == ["ym:s:date", "ym:s:visits"]

    assert response.data.values() == [
        ["2020-10-01", 14234.0],
        ["2020-10-02", 12508.0],
        ["2020-10-03", 12365.0],
        ["2020-10-04", 14588.0],
        ["2020-10-05", 14579.0],
    ]
    assert response.data.columns() == [
        ["2020-10-01", "2020-10-02", "2020-10-03", "2020-10-04", "2020-10-05"],
        [14234.0, 12508.0, 12365.0, 14588.0, 14579.0],
    ]
    assert response.data.dicts() == [
        {"ym:s:date": "2020-10-01", "ym:s:visits": 14234.0},
        {"ym:s:date": "2020-10-02", "ym:s:visits": 12508.0},
        {"ym:s:date": "2020-10-03", "ym:s:visits": 12365.0},
        {"ym:s:date": "2020-10-04", "ym:s:visits": 14588.0},
        {"ym:s:date": "2020-10-05", "ym:s:visits": 14579.0},
    ]


async def test_iteration(mocked, client):

    response_data = loads(REPORTS_DATA)

    url_1 = make_url(client.reports().path, url_params)

    url_2_params = dict(url_params)
    url_2_params["offset"] = url_params.get("offset", 1) + 1

    url_2 = make_url(client.reports().path, url_2_params)

    mocked.get(url_1, body=REPORTS_DATA, status=200, content_type="application/json")
    mocked.get(url_2, body=REPORTS_DATA, status=200, content_type="application/json")

    report = await client.reports().get(params=dict(url_params))

    i = 0
    max_pages = 1
    async for page in report().pages(max_pages=max_pages):

        assert page.data() == response_data
        assert page.data.headers() == ["ym:s:date", "ym:s:visits"]

        for row in page.data.values():
            assert len(row) == 2
            assert isinstance(row, list)
            assert isinstance(row[0], str)
            assert isinstance(row[1], float)

        for row in page.data.dicts():
            assert len(row) == 2
            assert isinstance(row, dict)
            assert isinstance(row["ym:s:date"], str)
            assert isinstance(row["ym:s:visits"], float)

        for index, row in enumerate(page.data.columns()):
            assert len(row) == 5
            assert isinstance(row, list)
            for item in row:
                if index == 0:
                    assert isinstance(item, str)
                elif index == 1:
                    assert isinstance(item, float)

        response_data["query"]["offset"] += response_data["query"]["offset"] + 1

        i += 1

    assert i == max_pages
