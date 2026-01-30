import aiosqlite
import json
from typing import Dict, Any
from datetime import date

async def save_daily_stats(db: aiosqlite.Connection, date: date, data: Dict[str, Any]) -> None:
    '''
    Сохраняет статистику Wakatime за день
    
    :param db: Соединение с базой данных
    :type db: aiosqlite.Connection
    :param date: Дата в формате 'YYYY-MM-DD'
    :type date: date
    :param data: Данные статистики за день
    :type data: Dict[str, Any]
    '''
    await db.execute("""
        INSERT OR IGNORE INTO wakatime (date, data) VALUES (?, ?)
        """,
        (
            date.isoformat(),
            json.dumps(data)
        ),
    )