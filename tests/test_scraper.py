import pytest
import aiohttp
import os


@pytest.mark.asyncio
async def test_parse_vacancies():
    async with aiohttp.ClientSession() as session:
        async with session.get(os.environ["SCRAPER_ROUTE"], params={"name": "ML"}) as response:
            assert response.status == 200
