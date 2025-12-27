import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/"
POSTER_PLACEHOLDER = "https://via.placeholder.com/500x750?text=Нет+постера"

async def search_media(query: str):
    if not OMDB_API_KEY:
        print("ОШИБКА: OMDB_API_KEY не найден в .env")
        return

    params = {
        "apikey": OMDB_API_KEY,
        "s": query.strip()
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OMDB_URL, params=params, timeout=30.0)
        print(f"Статус: {response.status_code}")
        data = response.json()

    if data.get("Response") == "False":
        print(f"Ошибка: {data.get('Error')}\n")
        return

    print(f"Найдено всего: {data.get('totalResults')}")
    for item in data.get("Search", []):
        media_type = "Сериал" if item.get("Type") == "series" else "Фильм"
        title = item.get("Title", "Без названия")
        year = item.get("Year", "?")
        poster = item.get("Poster") if item.get("Poster") != "N/A" else "Нет постера"
        print(f"• {title} ({year}) — {media_type}")
        print(f"  Постер: {poster[:80]}{'...' if len(poster) > 80 else ''}")
        print(f"  IMDb ID: {item.get('imdbID')}")
    print()

async def main():
    queries = [
        "Matrix 1999",
        "Interstellar",
        "Breaking Bad",
        "Harry Potter",
        "Dune 2021",
        "Avatar 2009",
        "Shrek 2001",
        "Dark Knight 2008"
    ]

    print("Тестируем OMDb API\n")
    for q in queries:
        print(f"Запрос: '{q}'")
        await search_media(q)

asyncio.run(main())