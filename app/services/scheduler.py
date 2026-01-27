from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.sporify_collector import collect_spotify_data

scheduler = AsyncIOScheduler()


def init_scheduler():
    """Инициализирует scheduler и добавляет задачи"""

    # Добавляем задачу: каждые 30 минут вызвать КАКАЯ-ТО_ФУНКЦИЯ
    scheduler.add_job(
        collect_spotify_data,
        "interval",  # Используем интервал
        minutes=30,  # Каждые 30 минут
        id="collect_spotify",  # Уникальный ID задачи
        name="Collect Spotify tracks",
        misfire_grace_time=10,  # Если вдруг пропустится — запустить в течение 10 сек
        coalesce=True,  # Если пропустились несколько запусков — запустить один раз
        next_run_time=datetime.now(),  # запускать сразу при старте планировщика
    )


def start_scheduler():
    """Запускает scheduler"""
    if not scheduler.running:
        scheduler.start()
        print("запущен scheduler")


def shutdown_scheduler():
    """Останавливает scheduler"""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("остановлен scheduler")
