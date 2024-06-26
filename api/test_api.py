import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from main import get_db

session = get_db()


@pytest.mark.asyncio
async def test_read_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://api") as ac:
        response = await ac.request(method="GET",
                                    url="/vacancies/",
                                    json={"hh_id": 1})
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://api") as ac:
        new_vacancy = {
            "hh_id": 12345,
            "name": "Test Vacancy",
            "area": "Test Area",
            "area_id": 67890,
            "salary_from": 50000,
            "salary_to": 70000,
            "url": "http://example.com",
            "requirement": "Test requirement",
            "responsibility": "Test responsibility",
            "employment": "full-time"
        }
        response = await ac.post("/vacancies/", json=new_vacancy)
        assert response.status_code == 200
