import pytest_asyncio
from response_data import COUNTERS_DATA, GOAL_DATA, GOALS_DATA

from aiotapioca_yandex_metrika import YandexMetrikaManagementAPI
from aiotapioca_yandex_metrika.aiotapioca_yandex_metrika import LIMIT


@pytest_asyncio.fixture
async def client():
    async with YandexMetrikaManagementAPI(access_token="token") as c:
        yield c


async def test_methods_exists(client):
    assert "accounts" in dir(client)
    assert "counters" in dir(client)
    assert "goals" in dir(client)


async def test_get_counters(mocked, client):
    mocked.get(
        client.counters().path + f"?per_page={LIMIT}",
        body=COUNTERS_DATA,
        status=200,
        content_type="application/json",
    )

    response = await client.counters().get()

    response_data = response.data()

    assert response.status == 200
    assert response_data["rows"] == 2
    assert len(response_data["counters"]) == 2
    assert response_data["counters"][0]["id"] == 12345678
    assert response_data["counters"][0]["name"] == "counter 1"
    assert response_data["counters"][1]["id"] == 87654321
    assert response_data["counters"][1]["name"] == "counter 2"


async def test_get_goals(mocked, client):
    mocked.get(
        client.goals(counter_id=12345648).path,
        body=GOALS_DATA,
        status=200,
        content_type="application/json",
    )

    response = await client.goals(counter_id=12345648).get()

    response_data = response.data()

    assert response.status == 200
    assert len(response_data["goals"]) == 2
    assert response_data["goals"][0]["id"] == 1234567
    assert response_data["goals"][0]["name"] == "goal 1"
    assert response_data["goals"][1]["id"] == 7654321
    assert response_data["goals"][1]["name"] == "goal 2"


async def test_get_goal(mocked, client):
    params = {"counter_id": 12345648, "goal_id": 1234567}

    mocked.get(
        client.goal(**params).path,
        body=GOAL_DATA,
        status=200,
        content_type="application/json",
    )

    response = await client.goal(**params).get()

    response_data = response.data()

    assert isinstance(response_data["goal"], dict)
    assert response_data["goal"]["id"] == 1234567
    assert response_data["goal"]["name"] == "goal 1"
