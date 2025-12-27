from fastapi import FastAPI

app = FastAPI(title="Личный трекер фильмов и сериалов")

@app.get("/")
def home():
    return {"message": "Трекер запущен! API готов к работе."}