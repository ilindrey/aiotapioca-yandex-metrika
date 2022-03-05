import json
from copy import deepcopy
from aioresponses import aioresponses, CallbackResult

from async_tapi_yandex_metrika import YandexMetrikaStats
from response_data import REPORTS_DATA
from utils import make_url


default_params = dict(access_token="token")

url_params = dict(
    ids=100500,
    metrics="ym:s:visits",
    dimensions="ym:s:date",
    sort="ym:s:date",
    filters="ym:s:startURL=.('https://rfgf.ru/map','https://rfgf.ru/map')",
    group="Day",
    date1="2020-10-01",
    date2="2020-10-05",
    limit=1,
)


async def test_get_help_info():
    async with YandexMetrikaStats(**default_params) as client:
        help_info = client.stats().help()
        assert (
            "https://yandex.ru/dev/metrika/doc/api2/api_v1/intro-docpage/" in help_info
        )
        assert "stat/v1/data" in help_info


async def test_stats_data():
    async with YandexMetrikaStats(**default_params) as client:
        with aioresponses() as mocked:

            mocked.get(
                make_url(client.stats().data, url_params),
                body=REPORTS_DATA,
                status=200,
                content_type="application/json",
            )

            response = await client.stats().get(params=url_params)

            assert response.data["query"]["ids"] == [100500]
            assert response.data["query"]["limit"] == 1
            assert len(response.data["data"]) > 0
            assert len(response.data["totals"]) > 0
            assert response.data["totals"][0] > 0


async def test_transform():
    async with YandexMetrikaStats(**default_params) as client:
        with aioresponses() as mocked:
            mocked.get(
                make_url(client.stats().data, url_params),
                body=REPORTS_DATA,
                status=200,
                content_type="application/json",
            )

            response = await client.stats().get(params=url_params)

            response_data = json.loads(REPORTS_DATA)

            assert response.data == response_data
            assert response().to_values() == [
                ["2020-10-01", 14234.0],
                ["2020-10-02", 12508.0],
                ["2020-10-03", 12365.0],
                ["2020-10-04", 14588.0],
                ["2020-10-05", 14579.0],
            ]
            assert response().to_columns() == [
                ["2020-10-01", "2020-10-02", "2020-10-03", "2020-10-04", "2020-10-05"],
                [14234.0, 12508.0, 12365.0, 14588.0, 14579.0],
            ]
            assert response().to_dicts() == [
                {"ym:s:date": "2020-10-01", "ym:s:visits": 14234.0},
                {"ym:s:date": "2020-10-02", "ym:s:visits": 12508.0},
                {"ym:s:date": "2020-10-03", "ym:s:visits": 12365.0},
                {"ym:s:date": "2020-10-04", "ym:s:visits": 14588.0},
                {"ym:s:date": "2020-10-05", "ym:s:visits": 14579.0},
            ]


async def test_iteration():
    response_data = json.loads(REPORTS_DATA)
    async with YandexMetrikaStats(**default_params) as client:
        url_1 = make_url(client.stats().data, url_params)

        url_2_params = dict(url_params)
        url_2_params["offset"] = url_params.get("offset", 1) + 1

        url_2 = make_url(client.stats().data, url_2_params)

        with aioresponses() as mocked:

            mocked.get(url_1, body=REPORTS_DATA, status=200, content_type="application/json")
            mocked.get(url_2, body=REPORTS_DATA, status=200, content_type="application/json")

            report = await client.stats().get(params=dict(url_params))

            i = 0
            max_pages = 1
            async for page in report().pages(max_pages=max_pages):
                assert page.data == response_data

                for row in page().values():
                    assert len(row) == 2
                    assert isinstance(row, list)
                    assert isinstance(row[0], str)
                    assert isinstance(row[1], float)

                for row in page().dicts():
                    assert len(row) == 2
                    assert isinstance(row, dict)
                    assert isinstance(row["ym:s:date"], str)
                    assert isinstance(row["ym:s:visits"], float)

                response_data["query"]["offset"] += response_data["query"]["offset"] + 1

                i += 1

            assert i == max_pages

        with aioresponses() as mocked:

            mocked.get(url_1, body=REPORTS_DATA, status=200, content_type="application/json")
            mocked.get(url_2, body=REPORTS_DATA, status=200, content_type="application/json")

            report = await client.stats().get(params=dict(url_params))

            i = 0
            async for row in report().iter_values(max_pages=1):
                assert len(row) == 2
                assert isinstance(row, list)
                assert isinstance(row[0], str)
                assert isinstance(row[1], float)
                i += 1
            assert i == len(response_data['data'])

        with aioresponses() as mocked:
            mocked.get(url_1, body=REPORTS_DATA, status=200, content_type="application/json")
            mocked.get(url_2, body=REPORTS_DATA, status=200, content_type="application/json")

            report = await client.stats().get(params=dict(url_params))

            i = 0
            async for row in report().iter_dicts(max_pages=1):
                assert len(row) == 2
                assert isinstance(row, dict)
                assert isinstance(row["ym:s:date"], str)
                assert isinstance(row["ym:s:visits"], float)
                i += 1
            assert i == len(response_data['data'])
