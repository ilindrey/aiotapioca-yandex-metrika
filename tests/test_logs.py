import json
from io import StringIO
from aioresponses import aioresponses

from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI
from response_data import LOGS_DATA
from utils import make_url


default_params = dict(
    access_token="token",
    default_url_params={"counterId": 100500},
    wait_report=True,
)


async def test_create():
    async with YandexMetrikaLogsAPI(**default_params) as client:
        with aioresponses() as mocked:
            response_data = {
                "log_request": {
                    "request_id": 12345678,
                    "counter_id": 100500,
                    "source": "visits",
                    "date1": "2020-12-01",
                    "date2": "2020-12-02",
                    "fields": ["ym:p:date"],
                    "status": "created",
                    "attribution": "LASTSIGN",
                }
            }
            url_params = {
                "fields": "ym:s:date",
                "source": "visits",
                "date1": "2020-12-01",
                "date2": "2020-12-02",
            }
            mocked.post(
                make_url(client.create().data, url_params),
                body=json.dumps(response_data, default=str),
                status=200,
                content_type="application/json",
            )
            response = await client.create().post(params=url_params)

            assert "log_request" in dir(response)
            assert response.log_request.status().data == "created"
            assert response.log_request.date1().data == url_params["date1"]
            assert response.log_request.date2().data == url_params["date2"]
            assert response().data == response_data


async def test_get_allinfo():
    response_data = {
        "requests": [
            {
                "request_id": 12345678,
                "counter_id": 100500,
                "source": "visits",
                "date1": "2020-12-01",
                "date2": "2020-12-02",
                "fields": ["ym:s:date"],
                "status": "processed",
                "size": 15555,
                "parts": [{"part_number": 0, "size": 15555}],
                "attribution": "LASTSIGN",
            },
            {
                "request_id": 87654321,
                "counter_id": 100500,
                "source": "hits",
                "date1": "2020-12-01",
                "date2": "2020-12-02",
                "fields": ["ym:pv:date"],
                "status": "processed",
                "size": 555555,
                "parts": [{"part_number": 0, "size": 555555}],
                "attribution": "LASTSIGN",
            },
        ]
    }
    async with YandexMetrikaLogsAPI(**default_params) as client:
        with aioresponses() as mocked:

            mocked.get(
                client.allinfo().data,
                body=json.dumps(response_data, default=str),
                status=200,
                content_type="application/json",
            )

            response = await client.allinfo().get()

            assert response().data == response_data


async def test_transform():
    async with YandexMetrikaLogsAPI(**default_params) as client:
        with aioresponses() as mocked:
            mocked.get(
                "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/0/part/0/download",
                body=LOGS_DATA,
                status=200,
            )
            log = await client.download(requestId=0).get()

            assert log().to_headers() == ["col1", "col2"]

            assert log().to_values() == [
                ["val1", "val2"],
                ["val11", "val22"],
                ["val111", "val222"],
                ["val1111", "val2222"],
            ]
            assert log().to_lines() == [
                "val1\tval2",
                "val11\tval22",
                "val111\tval222",
                "val1111\tval2222",
            ]
            assert log().to_columns() == [
                ["val1", "val11", "val111", "val1111"],
                ["val2", "val22", "val222", "val2222"],
            ]
            assert log().to_dicts() == [
                {"col1": "val1", "col2": "val2"},
                {"col1": "val11", "col2": "val22"},
                {"col1": "val111", "col2": "val222"},
                {"col1": "val1111", "col2": "val2222"},
            ]


async def test_iteration():

    columns = LOGS_DATA.split("\n")[0].split("\t")

    def _iter_line(text):
        f = StringIO(text)
        next(f)  # skipping columns
        return (line.replace("\n", "") for line in f)

    def to_columns(data):
        c = [[] for _ in range(len(columns))]
        for line in _iter_line(data):
            values = line.split("\t")
            for i, col in enumerate(c):
                col.append(values[i])
        return c

    expected_lines = LOGS_DATA.split("\n")[1:]
    expected_values = [i.split("\t") for i in LOGS_DATA.split("\n")[1:]]
    expected_columns = to_columns(LOGS_DATA)
    expected_dicts = [
        dict(zip(columns, i.split("\t"))) for i in LOGS_DATA.split("\n")[1:]
    ]

    url_1 = "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/0/part/0/download"
    url_2 = "https://api-metrika.yandex.net/management/v1/counter/100500/logrequest/0/part/1/download"

    async with YandexMetrikaLogsAPI(**default_params) as client:

        # parts
        with aioresponses() as mocked:

            mocked.get(url_1, body=LOGS_DATA, status=200)
            mocked.get(url_2, body=LOGS_DATA, status=200)

            log = await client.download(requestId=0).get()

            max_parts = 1
            async for part in log().pages(max_pages=max_parts):
                assert len(part().to_lines()) == 4
                assert len(part().to_values()) == 4
                assert len(part().to_columns()) == 2
                assert len(part().to_dicts()) == 4

                assert part().to_headers() == ["col1", "col2"]

                for line, expected in zip(part().to_lines(), expected_lines):
                    assert line == expected

                for values, expected in zip(part().to_values(), expected_values):
                    assert values == expected

                for values, expected in zip(part().to_columns(), expected_columns):
                    assert values == expected

                for values, expected in zip(part().to_dicts(), expected_dicts):
                    assert values == expected


"""

Old tests, fixes needed


def test_download():
    report = api.download(requestId=request_id).get()
    for part in report().parts(max_parts=2):
        for line in part().lines(max_rows=2):
            print("line", line)

        print("part", part().to_values()[:1])
        print("part", part().to_lines()[:1])

    print("report", report().to_values()[:1])
    print("report", report().to_lines()[:1])


def test_iter():
    report = api.download(requestId=request_id).get()
    for line in report().iter_lines(max_rows=2):
        print("line", line)

    for values in report().iter_values(max_rows=2):
        print("values", values)


def test_get_info():
    r = api.info(requestId=request_id).get()
    print(r)


def test_clean():
    request_id = test_create()
    while True:
        r = api.info(requestId=request_id).get()
        if r.data["log_request"]["status"] == "processed":
            break
        time.sleep(5)

    r = api.clean(requestId=request_id).post()
    print(r)


def test_cancel():
    request_id = test_create()
    r = api.cancel(requestId=request_id).post()
    print(r)

"""
