import os
import json
import aiofiles
from typing import Optional


SYNC_STATE_FILE = "app/db/sync_state.json"


async def ensure_sync_state_file_exists() -> None:
    """Проверяет, что файл состояния существует, и создает его, если его нет."""
    if not os.path.exists(SYNC_STATE_FILE):
        async with aiofiles.open(SYNC_STATE_FILE, "w") as f:
            await f.write(json.dumps({"after": None}, indent=2))


async def get_after() -> Optional[int]:
    """Получает значение after для следующего запроса"""
    try:
        async with aiofiles.open(SYNC_STATE_FILE, "r") as f:
            data = json.loads(await f.read())
            return data.get("after")
    except FileNotFoundError:
        return None


async def update_after(after: int) -> None:
    """Обновляет значение after"""
    async with aiofiles.open(SYNC_STATE_FILE, "w") as f:
        await f.write(json.dumps({"after": after}, indent=2))
