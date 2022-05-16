# Documentation for downloading reports from Yandex Metrika LOGS API

[Official documentation Yandex Metrika LOGS API](https://yandex.com/dev/metrika/doc/api2/api_v1/data.html)

```python
from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI

ACCESS_TOKEN = ""
COUNTER_ID = ""

params = {
    "fields": "ym:s:date,ym:s:clientID",
    "source": "visits",
    "date1": "2021-01-01",
    "date2": "2021-01-01"
    }

async with YandexMetrikaLogsAPI(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID}
    ) as client:
    # Check the possibility of creating a report. Via HTTP GET method.
    result = await client.evaluate().get(params=params)
    print(result)

    # Order a report. Via HTTP POST method.
    result = await client.create().post(params=params)
    request_id = result().data["log_request"]["request_id"]
    print(result)

    # Cancel report creation. Via HTTP POST method.
    result = await client.cancel(requestId=request_id).post()
    print(result)

    # Delete report. Via HTTP POST method.
    result = await client.clean(requestId=request_id).post()
    print(result)

    # Get information about all reports stored on the server. Via HTTP GET method.
    result = await client.allinfo().get()
    print(result)

    # Get information about a specific report. Via HTTP GET method.
    result = await client.info(requestId=request_id).get()
    print(result)

    # Download the report. Via HTTP POST method.
    result = await client.create().post(params=params)
    request_id = result["log_request"]["request_id"]

    # The report can be downloaded when it is generated on the server. Via HTTP GET method.
    info = await client.info(requestId=request_id).get()
    if info["log_request"]["status"] == "processed":

        # The report can consist of several parts.
        parts = info["log_request"]["parts"]
        print("Number of parts in the report", parts)

        # The partNumber parameter specifies the number of the part of the report that you want to download.
        # Default partNumber=0
        part = await client.download(requestId=request_id, partNumber=0).get()

        executor = part()

        print("Raw data")
        data = executor.data[:1000]

        print("Column names")
        print(executor.headers())

        # Transform to values
        print(executor.values()[:3])

        # Transform to lines
        print(executor.lines()[:3])

        # Transform to dicts
        print(executor.dicts()[:3])

        # Transform to columns
        print(executor.columns()[:3])
    else:
        print("Report not ready yet")
```

## Automatically download the report when it is prepared

add param **wait_report**

```python
from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI

ACCESS_TOKEN = ""
COUNTER_ID = ""

params = {
    "fields": "ym:s:date,ym:s:clientID,ym:s:dateTime,ym:s:startURL,ym:s:endURL",
    "source": "visits",
    "date1": "2019-01-01",
    "date2": "2019-01-01"
    }
async with YandexMetrikaLogsAPI(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID},
    # Download the report when it will be created
    wait_report=True,
    ) as client:
    info = await client.create().post(params=params)
    request_id = info["log_request"]["request_id"]

    report = await client.download(requestId=request_id).get()

    executor = report()

    print("Raw data")
    data = executor.data

    print("Column names")
    print(executor.headers())

    # Transform to values
    print(executor.values())

    # Transform to lines
    print(executor.lines())

    # Transform to dict
    print(executor.dicts())

    # Transform to columns
    print(executor.columns())
```

## Export of all report parts.

```python
from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI

async with YandexMetrikaLogsAPI(...) as client:
    info = await client.create().post(params=...)
    request_id = info["log_request"]["request_id"]
    report = await client.download(requestId=request_id).get()

    print(report.columns)

    # Iteration parts.
    async for part in report().page():
        executor = part()
        print(executor.data)  # raw data
        print(executor.values())
        print(executor.lines())
        print(executor.columns())  # columns data orient
        print(executor.dicts())

    async for part in report().page():
        # Iteration lines.
        for row_as_text in part().lines():
            print(row_as_text)

        # Iteration values.
        for row_as_values in part().values():
            print(row_as_values)

        # Iteration dicts.
        for row_as_dict in part().dicts():
            print(row_as_dict)


```

## Limit iteration

    .pages(max_pages: int = None, max_items: int = None)

## Response

```python

from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI

async with YandexMetrikaLogsAPI(...) as client:
    info = await client.create().post(params=...)

    executor = info()
    print(executor.data)
    print(executor.response)
    print(executor.response.headers)
    print(executor.status)

    report = await client.download(requestId=info["log_request"]["request_id"]).get()
    async for part in report().pages():
        executor = part()
        print(executor.data)
        print(executor.response)
        print(executor.response.headers)
        print(executor.response.status)
```

## Warning
Pay attention to which HTTP method you send the request.
Some resources work only with POST or only with GET requests.
For example create resource with POST method only

    await client.create().post(params=params)

And evaluate method only with GET method

    await client.evaluate().get(params=params)
