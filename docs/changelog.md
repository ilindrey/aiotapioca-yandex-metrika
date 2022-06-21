
# CHANGELOG

## Release 2022.6.22

- Added a py.typed merker for type hints

## Release 2022.6.15

- Drop support Python 3.6 and below
- Updated aiotapioca-wrapper library to version 4.0.0. Drop support aiotapioca-wrapper 3.8.0 and below
- Renamed YandexMetrikaDownloadReportError -> YandexMetrikaDownloadLogError
- Reworked exception handling v.2
- Minor fixes

## Release 2022.5.16

- Updated aiotapioca-wrapper library to version 3.8.0. Drop support aiotapioca-wrapper 3.7.0 and below
- Added generic change log file
- Added YandexMetrikaServerError
- Added conversion of date1 and date2 to a string in the appropriate format
- Added support for pagination when requesting counters
- Changed output to debug level in YandexMetrikaStatsClientAdapter.process_response
- Reworked exception handling
- Renamed clients YandexMetrikaManagement -> YandexMetrikaManagementAPI and YandexMetrikaStats -> YandexMetrikaReportsAPI
- Replaced serializers with data parsers
- Replaced setup.cfg with pyproject.toml

## Release 2022.4.23

- Updated aiotapioca-wrapper library to version 3.6.0. Drop support aiotapioca-wrapper 3.5.0 and below

## Release 2022.4.13

### Logs API
- Changes related to the original library [commit](https://github.com/pavelmaksimov/tapi-yandex-metrika/commit/db8e6b09643e553bce865e8ee4199c0756635f9c). Stop waiting a report if the report status is invalid by raising an error

## Release 2022.3.26

- An asynchronous fork was created. The original library became asynchronous, based on aiotapioca-wrapper

## Release 2021.5.28

- Add stub file (syntax highlighting)

## Release 2021.5.15

### Reports API

- add iteration method "iter_values"
- add iteration method "iter_dicts"
- add iteration method "values"
- add iteration method "dicts"
- add method "to_dicts"
- rename parameter max_items to max_rows in iter_rows

### Logs API

- add iteration method "dicts"
- add iteration method "iter_dicts"
- add method "to_dicts"
- rename parameter max_items to max_rows in iter_lines, iter_values, lines, values


## Release 2021.2.21

### Management API

- New feature:
  - add attribut "data"
  - add attribut "response"

### Reports API

- Backward incompatible change:
  - drop method "transform"
  - drop param "receive_all_data"
- New feature:
  - translated into english
  - add iteration method "pages"
  - add iteration method "rows"
  - add iteration method "iter_rows"
  - add attribut "columns"
  - add attribut "data"
  - add attribut "response"
  - add method "to_values"
  - add method "to_columns"

### Logs API

- Backward incompatible change:
  - drop method "transform"
  - drop param "receive_all_data"
- New feature:
  - translated into english
  - add iteration method "parts"
  - add iteration method "lines"
  - add iteration method "values"
  - add iteration method "iter_lines"
  - add iteration method "iter_values"
  - add attribut "columns"
  - add attribut "data"
  - add attribut "response"
  - add method "to_lines"
  - add method "to_values"
  - add method "to_columns"
