# точка входа в приложение FastAPI
from fastapi import FastAPI
from app.core.config import (
    REFRESH_TOKEN,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    DB_PATH,
)

from app.services.scheduler import init_scheduler, start_scheduler, shutdown_scheduler
from scripts.init_db import init_db

app = FastAPI(title="TG Spotify Statistics API")


print("Переменные окружения:")
print(f"REFRESH_TOKEN={REFRESH_TOKEN}")
print(f"SPOTIFY_CLIENT_ID={SPOTIFY_CLIENT_ID}")
print(f"SPOTIFY_CLIENT_SECRET={SPOTIFY_CLIENT_SECRET}")
print(f"DB_PATH={DB_PATH}")


@app.on_event("startup")
async def on_startup():
    """Действия при старте приложения"""
    init_scheduler()
    await init_db(DB_PATH)
    start_scheduler()


@app.on_event("shutdown")
async def on_shutdown():
    """Действия при остановке приложения"""
    shutdown_scheduler()
