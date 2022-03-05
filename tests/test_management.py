import json
import pytest
from aioresponses import aioresponses, CallbackResult

from async_tapi_yandex_metrika import YandexMetrikaManagement
from response_data import COUNTERS_DATA, GOALS_DATA, GOAL_DATA


default_params = dict(access_token="token")


async def test_methods_exists():
    client = YandexMetrikaManagement(**default_params)

    assert "accounts" in dir(client)
    assert "counters" in dir(client)
    assert "goals" in dir(client)


async def test_get_counters():
    async with YandexMetrikaManagement(**default_params) as client:
        with aioresponses() as mocked:

            mocked.get(
                client.counters().data,
                body=COUNTERS_DATA,
                status=200,
                content_type="application/json",
            )

            response = await client.counters().get()

            assert response.status == 200
            assert response.data["rows"] == 2
            assert len(response.data["counters"]) == 2
            assert response.data["counters"][0]["id"] == 12345678
            assert response.data["counters"][0]["name"] == "counter 1"
            assert response.data["counters"][1]["id"] == 87654321
            assert response.data["counters"][1]["name"] == "counter 2"


async def test_get_goals():
    async with YandexMetrikaManagement(**default_params) as client:
        with aioresponses() as mocked:

            mocked.get(
                client.goals(counterId=12345648).data,
                body=GOALS_DATA,
                status=200,
                content_type="application/json",
            )

            response = await client.goals(counterId=12345648).get()

            assert response.status == 200
            assert len(response.data["goals"]) == 2
            assert response.data["goals"][0]["id"] == 1234567
            assert response.data["goals"][0]["name"] == "goal 1"
            assert response.data["goals"][1]["id"] == 7654321
            assert response.data["goals"][1]["name"] == "goal 2"


async def test_get_goal():
    async with YandexMetrikaManagement(**default_params) as client:
        with aioresponses() as mocked:

            params = {"counterId": 12345648, "goalId": 1234567}

            mocked.get(
                client.goal(**params).data,
                body=GOAL_DATA,
                status=200,
                content_type="application/json",
            )

            response = await client.goal(**params).get()

            assert isinstance(response.data["goal"], dict)
            assert response.data["goal"]["id"] == 1234567
            assert response.data["goal"]["name"] == "goal 1"
