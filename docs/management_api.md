# Yandex Metrika Management API Documentation

[Official documentation Yandex Metrika Management API](https://yandex.com/dev/metrika/doc/api2/management/intro.html)


```python
from aiotapioca_yandex_metrika import YandexMetrikaManagementAPI

ACCESS_TOKEN = ""
COUNTER_ID = ""

async with YandexMetrikaManagementAPI(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID}
) as client:
```

### Resources
```python
print(dir(client))
['accounts', 'chart_annotation', 'chart_annotations', 'clients', 'counter', 'counter_undelete',
 'counters', 'delegate', 'delegates', 'filter', 'filters', 'goal', 'goals', 'grant', 'grants', 'label',
 'labels', 'offline_conversions_calls_extended_threshold', 'offline_conversions_calls_uploading',
 'offline_conversions_calls_uploadings', 'offline_conversions_extended_threshold',
 'offline_conversions_upload', 'offline_conversions_upload_calls', 'offline_conversions_uploading',
 'offline_conversions_uploadings', 'operation', 'operations', 'public_grant', 'segment', 'segments',
 'set_counter_label', 'user_params_upload', 'user_params_uploading', 'user_params_uploading_confirm',
 'user_params_uploadings', 'yclid_conversions_upload', 'yclid_conversions_uploading',
 'yclid_conversions_uploadings']

# Open resource documentation in a browser
client.counters().open_docs()
```

How to send different types of HTTP requests

:param params: querystring arguments in the URL\
:param data: send data in the body of the request
```python
# Send HTTP 'GET' request
await client.counters().get(data: dict = None, params: dict = None)
# Send HTTP 'POST' request
await client.counters().post(data: dict = None, params: dict = None)
# Send HTTP 'DELETE' request
await client.counters().delete(data: dict = None, params: dict = None)
# Send HTTP 'PUT' request
await client.counters().put(data: dict = None, params: dict = None)
# Send HTTP 'PATCH' request
await client.counters().patch(data: dict = None, params: dict = None)
# Send HTTP 'OPTIONS' request
await client.counters().options(data: dict = None, params: dict = None)
```

```python
from aiotapioca_yandex_metrika import YandexMetrikaManagementAPI

async with YandexMetrikaManagementAPI(...) as client:

    # Get counters. Via HTTP GET method.
    counters = await client.counters().get()
    async for page in counters().pages():
        print(page().data)

    # Get counters sorted by visit. Via HTTP GET method.
    counters = await client.counters().get(params={"sort": "Visits"})
    print(counters().data)

    # Create a goal. Via HTTP POST method.
    body = {
            "goal": {
                "name": "2 страницы",
                "type": "number",
                "is_retargeting": 0,
                "depth": 2
            }
        }
    await client.goals().post(data=body)

    # Create target on JavaScript event. Via HTTP POST method.
    body2 = {
        "goal": {
            "name": "Название вашей цели в метрике",
            "type": "action",
            "is_retargeting": 0,
            "conditions": [
                    {
                        "type": "exact",
                        "url": <your_value>
                    }
                ]
            }
        }
    await client.goals().post(data=body2)

    # For some resources, you need to substitute the object identifier in the url.
    # This is done by adding an identifier to the method itself.
    # Get information about the target. Via HTTP GET method.
    await client.goal(goalId=10000).get()

    # Change target. Via HTTP PUT method.
    body = {
        "goal" : {
            "id" : <int>,
            "name" :  <string> ,
            "type" :  <goal_type>,
            "is_retargeting" :  <boolean>,
            ...
        }
    }
    await client.goal(goalId=10000).put(data=body)

    # Delete target. Via HTTP DELETE method.
    await client.goal(goalId=10000).delete()
```

You can get information about the request.
```python
counters = await client.counters().get()
executor = counters()
print(executor.data)
print(executor.response)
print(executor.response.headers)
print(executor.status)
```
