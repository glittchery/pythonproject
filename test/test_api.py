import pytest
from httpx import AsyncClient, ASGITransport

from lesson1 import app

@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        responce = await ac.get("/books")
        assert responce.status_code == 200
        data = responce.json()
        assert len(data) == 2


@pytest.mark.asyncio
async def test_post_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        responce = await ac.post("/books", json={
            "title": "Nazvanie",
            "author": "Author",
        })
        assert responce.status_code == 200
        data = responce.json()
        assert data == {"success": True, "message": "Книга успешно добавлена"}