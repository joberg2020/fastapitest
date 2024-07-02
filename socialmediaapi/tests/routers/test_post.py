import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    # pytest will check if there is an async_client here, then looks after conftest
    # in any parentfolder. It will eventually find our asyncclient-fixture in conftest.py
    # it is going to call it and give us the async_client
    return await create_post("Test Post yo!")


# we will use it like this:
# def test_post_something(created_post):
# This test already has created a post, and we have access to
# the API-response in here (in "created_post").
#


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post uno"
    response = await async_client.post("/post", json={"body": body})
    assert response.status_code == 201
    assert {"id": 0, "body": body}.items() <= response.json().items()
