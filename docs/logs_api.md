# Yandex Metrika Logs API Documentation

[Official documentation Yandex Metrika Logs API](https://yandex.com/dev/metrika/doc/api2/api_v1/intro.html)

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

client = YandexMetrikaLogsAPI(
    access_token=ACCESS_TOKEN,
    default_url_params={'counter_id': COUNTER_ID}
    )

# Check the possibility of creating a report. Via HTTP GET method.
result = await client.evaluate().get(params=params)
print(result)

# Order a report. Via HTTP POST method.
result = await client.create().post(params=params)
request_id = result.data()["log_request"]["request_id"]
print(result)

# Cancel report creation. Via HTTP POST method.
result = await client.cancel(request_id=request_id).post()
print(result)

# Delete report. Via HTTP POST method.
result = await client.clean(request_id=request_id).post()
print(result)

# Get information about all reports stored on the server. Via HTTP GET method.
result = await client.allinfo().get()
print(result)

# Get information about a specific report. Via HTTP GET method.
result = await client.info(request_id=request_id).get()
print(result)

# Download the report. Via HTTP POST method.
result = await client.create().post(params=params)
# Similarly result.data()["log_request"]["request_id"]
request_id = result.data.log_request.request_id()

# The report can be downloaded when it is generated on the server. Via HTTP GET method.
info = await client.info(request_id=request_id).get()
info_data = info.data()
if info_data["log_request"]["status"] == "processed":

    # The report can consist of several parts.
    parts = info_data["log_request"]["parts"]
    print("Number of parts in the report", parts)

    # The part_number parameter specifies the number of the part of the report that you want to download.
    # Default part_number=0
    part = await client.download(request_id=request_id, part_number=0).get()

    print("Raw data")
    data = part.data()[:1000]

    print("Column names")
    print(part.data.headers())

    # Transform to values
    print(part.data.values()[:3])

    # Transform to lines
    print(part.data.lines()[:3])

    # Transform to dicts
    print(part.data.dicts()[:3])

    # Transform to columns
    print(part.data.columns()[:3])
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

client = YandexMetrikaLogsAPI(
    access_token=ACCESS_TOKEN,
    default_url_params={'counter_id': COUNTER_ID},
    # Download the report when it will be created
    wait_report=True,
    )


info = await client.create().post(params=params)
request_id = info.data.log_request.request_id()

report = await client.download(request_id=request_id).get()

print("Raw data")
data = report.data()

print("Column names")
print(report.data.headers())

# Transform to values
print(report.data.values())

# Transform to lines
print(report.data.lines())

# Transform to dict
print(report.data.dicts())

# Transform to columns
print(report.data.columns())
```

## Export of all report parts.

```python
from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI

client =  YandexMetrikaLogsAPI(...)

info = await client.create().post(params=...)
request_id = info.data.log_request.request_id()
report = await client.download(request_id=request_id).get()

print(report.columns)

# Iteration parts.
async for part in report().page():
    print(part.data())  # raw data
    print(part.data.values())
    print(part.data.lines())
    print(part.data.columns())  # columns data orient
    print(part.data.dicts())

async for part in report().page():
    # Iteration lines.
    for row_as_text in part.data.lines():
        print(row_as_text)

    # Iteration values.
    for row_as_values in part.data.values():
        print(row_as_values)

    # Iteration dicts.
    for row_as_dict in part.data.dicts():
        print(row_as_dict)


```

## Limit iteration

    .pages(max_pages: int = None, max_items: int = None)

## Response

```python

from aiotapioca_yandex_metrika import YandexMetrikaLogsAPI

client =  YandexMetrikaLogsAPI(...)

info = await client.create().post(params=...)

print(info.data())
print(info.response)
print(info.response.headers)
print(info.status)

report = await client.download(request_id=info["log_request"]["request_id"]).get()
async for part in report().pages():
    print(part.data())
    print(part.response)
    print(part.response.headers)
    print(part.response.status)
```

## Warning
Pay attention to which HTTP method you send the request.
Some resources work only with POST or only with GET requests.
For example create resource with POST method only

    await client.create().post(params=params)

And evaluate method only with GET method

    await client.evaluate().get(params=params)
