from fastapi import FastAPI, Query
import httpx
from .tmdb import search_media

app = FastAPI(title="Личный трекер фильмов и сериалов")

@app.get("/")
def home():
    return {"message": "Трекер запущен! API готов к работе."}

@app.get("/search")
async def search(q: str = Query(..., description="Название фильма или сериала"), page: int = 1):
    # поиск фильмов и сериалов в tmdb
    try:
        results = await search_media(q, page)
        return results
    except httpx.HTTPStatusError as e:
        return {"error": f"error tmdb api: {e.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
    