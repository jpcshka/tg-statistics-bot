from typing import AsyncGenerator
from contextlib import asynccontextmanager
import aiosqlite
from app.core.config import DB_PATH


@asynccontextmanager
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    if not DB_PATH:
        raise ValueError("DB_PATH не задан")
    async with aiosqlite.connect(DB_PATH) as db:
        yield db
