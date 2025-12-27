import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/"
POSTER_PLACEHOLDER = "https://via.placeholder.com/500x750?text=Нет+постера"

async def search_media(query: str):
    if not OMDB_API_KEY:
        raise Exception("OMDB_API_KEY не указан в .env")

    if len(query.strip()) < 3:
        return {
            "results": [],
            "total_results": 0,
            "error": "Запрос слишком короткий (минимум 3 символа)"
        }

    params = {
        "apikey": OMDB_API_KEY,
        "s": query.strip()
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OMDB_URL, params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()

    if data.get("Response") == "False":
        error_msg = data.get("Error", "Неизвестная ошибка OMDb")
        if "Too many results" in error_msg:
            error_msg = "Слишком много результатов — добавь год или больше деталей (например, 'Matrix 1999')"
        return {
            "results": [],
            "total_results": 0,
            "error": error_msg
        }

    total_results = int(data.get("totalResults", 0))
    results = []

    for item in data.get("Search", []):
        media_type = "tv" if item.get("Type") == "series" else "movie"
        title = item.get("Title", "Без названия")
        year = item.get("Year", "Год неизвестен")
        poster_url = item.get("Poster") if item.get("Poster") != "N/A" else POSTER_PLACEHOLDER

        results.append({
            "imdb_id": item.get("imdbID"),
            "title": title,
            "year": year,
            "media_type": media_type,
            "overview": "",
            "poster_url": poster_url
        })

    return {
        "total_results": total_results,
        "results": results
    }