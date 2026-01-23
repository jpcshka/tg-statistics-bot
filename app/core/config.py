# читаем env-файл и загружаем переменные окружения
import os
from dotenv import load_dotenv

load_dotenv()

REFRESH_TOKEN=os.getenv("REFRESH_TOKEN")
SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
DB_PATH=os.getenv("DB_PATH")

if not all([REFRESH_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, DB_PATH]):
    raise ValueError("Проверьте, что все переменные окружения заданы в .env файле")
