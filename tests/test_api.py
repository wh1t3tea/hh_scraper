import os
import pytest
import aiohttp
import asyncio


@pytest.mark.asyncio
async def test_create_data():
    _sem = asyncio.Semaphore(1)

    async with _sem:  # next coroutine(s) will stuck here until the previous is done
        await asyncio.sleep(1)
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        new_vacancy = {
            "hh_id": 12346,
            "name": "Test Vacancy",
            "area": "Test Area",
            "area_id": 67890,
            "salary_from": 50000,
            "salary_to": 70000,
            "url": "http://example.comm",
            "requirement": "Test requirement",
            "responsibility": "Test responsibility",
            "employment": "full-time",
            "text": "python backend"
        }
        async with session.post(os.environ["API_ROUTE"], json=new_vacancy) as response:
            assert response.status == 200


@pytest.mark.asyncio
async def test_read_data():
    _sem = asyncio.Semaphore(1)

    async with _sem:  # next coroutine(s) will stuck here until the previous is done
        await asyncio.sleep(1)

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(os.environ["API_ROUTE"], params={"hh_id": 12346}) as response:
            assert response.status == 200
