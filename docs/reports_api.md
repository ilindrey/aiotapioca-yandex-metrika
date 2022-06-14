# Yandex Metrika Reports API Documentation

[Official documentation Yandex Metrika Reports API](https://yandex.com/dev/metrika/doc/api2/api_v1/intro.html)

```python
from datetime import date
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

ACCESS_TOKEN = ""
COUNTER_ID = ""

client = YandexMetrikaReportsAPI(access_token=ACCESS_TOKEN)

params = dict(
    ids=COUNTER_ID,
    date1="2020-10-01",
    date2=date(2020, 10, 5),
    metrics="ym:s:visits",
    dimensions="ym:s:date",
    sort="ym:s:date",
    lang="en",
    # Other params -> https://yandex.com/dev/metrika/doc/api2/api_v1/data.html
    )
report = await client.reports().get(params=params)

# Raw data
print(report.data())
print(report.data.query.ids())
print(report.data.query.limit())
print(report.data.data())
print(report.data.totals())

print(report.data.headers())
# ['ym:s:date', 'ym:s:visits']

report.data.values()
# [
#    ['2020-10-01', 14234.0],
#    ['2020-10-02', 12508.0],
#    ['2020-10-03', 12365.0],
#    ['2020-10-04', 14588.0],
#    ['2020-10-05', 14579.0]
# ]

report.data.dicts()
# [
#     {"ym:s:date": "2020-10-01", "ym:s:visits": 14234.0},
#     {"ym:s:date": "2020-10-02", "ym:s:visits": 12508.0},
#     {"ym:s:date": "2020-10-03", "ym:s:visits": 12365.0},
#     {"ym:s:date": "2020-10-04", "ym:s:visits": 14588.0},
#     {"ym:s:date": "2020-10-05", "ym:s:visits": 14579.0},
# ]

# Column data orient
report.data.columns()
# [
#    ['2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05'],
#    [14234.0, 12508.0, 12365.0, 14588.0, 14579.0]
# ]

```

## Export of all report pages.

```python
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

client = YandexMetrikaReportsAPI(access_token=...)

report = await client.reports().get(params=...)

print("iteration report pages")
async for page in report().pages():

    # Raw data.
    print(page.data())
    print(page.data.dicts())
    print(page.data.columns())
    print(page.data.values())

print("iteration report pages")
async for page in report().pages():
    print("iteration rows as values")
    for row_as_values_of_page in page.data.values():
        print(row_as_values_of_page)
    # ['2020-10-01', 14234.0]
    # ['2020-10-02', 12508.0]
    # ['2020-10-03', 12365.0]
    # ['2020-10-04', 14588.0]
    # ['2020-10-05', 14579.0]
    # ['2020-10-06', 12795.0]

    print("iteration rows as dict")
    for row_as_dict_of_page in page.data.dicts():
        print(row_as_dict_of_page)

    print("iteration rows as column")
    for row_as_dict_of_page in page.data.columns():
        print(row_as_dict_of_page)
```

## Iteration limit.

    .pages(max_pages: int = None, max_items: int = None)

```python
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

client = YandexMetrikaReportsAPI(access_token=...)

report = await client.reports().get(params=...)

print("iteration report rows with limit")
async for page in report().pages(max_pages=2):
    for values in page.data.values():
        print(values)
# ['2020-10-01', 14234.0]
# ['2020-10-02', 12508.0]
# ['2020-10-06', 12795.0]
```

## Response
```python
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

client = YandexMetrikaReportsAPI(access_token=...)

report = await client.reports().get(params=...)

print(report.data())
print(report.response)
print(report.response.status)
print(report.response.headers)

async for page in report().pages():
    print(page.data())
    print(page.response)
    print(page.response.status)
    print(page.response.headers)
```
