import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_parse_vacancies():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://scraper_tests") as ac:
        response = await ac.request(method="GET",
                                    url="/parse/",
                                    json={"name": "ML"})
        assert response.status_code == 200
        assert "items" in response.json()
