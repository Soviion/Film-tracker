import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # для постеров

async def search_media(query: str, page: int = 1):
    """
    Ищет фильмы и сериалы по названию
    """
    url = f"{TMDB_BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "page": page,
        "language": "ru-RU",  # можно потом сделать en-US или динамически
        "include_adult": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    # Обрабатываем результаты
    results = []
    for item in data.get("results", []):
        media_type = item.get("media_type")
        if media_type not in ["movie", "tv"]:
            continue

        title = item.get("title") or item.get("name") or "Без названия"
        release_date = item.get("release_date") or item.get("first_air_date") or ""
        year = release_date.split("-")[0] if release_date else "Год неизвестен"

        poster_path = item.get("poster_path")
        poster_url = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None

        results.append({
            "tmdb_id": item["id"],
            "title": title,
            "year": year,
            "media_type": media_type,  # "movie" или "tv"
            "overview": item.get("overview", ""),
            "poster_url": poster_url
        })

    return {
        "page": data["page"],
        "total_pages": data["total_pages"],
        "total_results": data["total_results"],
        "results": results
    }