import httpx
from .omdb import search_media
from fastapi import FastAPI, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .omdb import search_media
from .crud import create_watched_item, get_user_list
from .schemas import WatchedItemCreate, WatchedItemResponse


app = FastAPI(title="Личный трекер фильмов и сериалов")

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Зависимость для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Временный пользователь (потом сделаем регистрацию)
CURRENT_USER_ID = 1

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    my_list = get_user_list(db, CURRENT_USER_ID)
    return templates.get_template("index.html").render({
        "request": request,
        "my_list": my_list
    })

@app.get("/api/search")
async def api_search(
    q: str = Query(..., description="Название"),
    type: str = Query(None, description="movie, series или пусто"),
    year: int = Query(None, description="Год выпуска")
):
    return await search_media(q, type, year)

@app.post("/api/my-list")
async def add_to_list(item: WatchedItemCreate, db: Session = Depends(get_db)):
    result = create_watched_item(db, item, CURRENT_USER_ID)
    if not result:
        raise HTTPException(400, "Этот фильм/сериал уже в вашем списке")
    return result
    