# Documentation for downloading reports from API Yandex Metrika.

[Official documentation API Yandex Metrika](https://yandex.com/dev/metrika/doc/api2/api_v1/data.html)

```python
from datetime import date
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

ACCESS_TOKEN = ""
COUNTER_ID = ""

async with YandexMetrikaReportsAPI(access_token=ACCESS_TOKEN) as client:

    params = dict(
        ids=COUNTER_ID,
        date1="2020-10-01",
        date2=date(2020,10,5),
        metrics="ym:s:visits",
        dimensions="ym:s:date",
        sort="ym:s:date",
        lang="en",
        # Other params -> https://yandex.com/dev/metrika/doc/api2/api_v1/data.html
    )
    report = await client.reports().get(params=params)

    # Raw data
    print(report().data)
    print(report.query.ids().data)
    print(report.query.limit().data)
    print(report.data().data)
    print(report.totals().data)


    print(report().to_headers())
    # ['ym:s:date', 'ym:s:visits']

    report().to_values()
    #[
    #    ['2020-10-01', 14234.0],
    #    ['2020-10-02', 12508.0],
    #    ['2020-10-03', 12365.0],
    #    ['2020-10-04', 14588.0],
    #    ['2020-10-05', 14579.0]
    #]

    report().to_dicts()

    # Column data orient
    report().to_columns()
    #[
    #    ['2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05'],
    #    [14234.0, 12508.0, 12365.0, 14588.0, 14579.0]
    #]

```

## Export of all report pages.
```python
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

async with YandexMetrikaReportsAPI(access_token=...) as client:
    report = await client.reports().get(params=...)

    print("iteration report pages")
    async for page in report().pages():
        executor = page()

        # Raw data.
        print(executor.data)

        print(executor.to_dicts())
        print(executor.to_columns())
        print(executor.to_values())

    print("iteration report pages")
    async for page in report().pages():
        print("iteration rows as values")
        for row_as_values_of_page in page().to_values():
            print(row_as_values_of_page)
        # ['2020-10-01', 14234.0]
        # ['2020-10-02', 12508.0]
        # ['2020-10-03', 12365.0]
        # ['2020-10-04', 14588.0]
        # ['2020-10-05', 14579.0]
        # ['2020-10-06', 12795.0]

        print("iteration rows as dict")
        for row_as_dict_of_page in page().to_dicts():
            print(row_as_dict_of_page)

        print("iteration rows as column")
        for row_as_dict_of_page in page().to_columns():
            print(row_as_dict_of_page)
```

## Iteration limit.

    .pages(max_pages: int = None, max_items: int = None)

```python
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

async with YandexMetrikaReportsAPI(access_token=...) as client:

    report = await client.reports().get(params=...)

    print("iteration report rows with limit")
    async for page in report().pages(max_pages=2):
        for values in page().to_values():
            print(values)
    # ['2020-10-01', 14234.0]
    # ['2020-10-02', 12508.0]
    # ['2020-10-06', 12795.0]
```

## Response
```python
from aiotapioca_yandex_metrika import YandexMetrikaReportsAPI

async with YandexMetrikaReportsAPI(access_token=...) as client:

    report = await client.reports().get(params=...)

    executor = report()
    print(executor.data)
    print(executor.response)
    print(executor.response.status)
    print(executor.response.headers)

    async for page in report().pages():
        executor = page()
        print(executor.data)
        print(executor.response)
        print(executor.response.status)
        print(executor.response.headers)
```
