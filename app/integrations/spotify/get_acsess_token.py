import httpx
import base64
import json
from typing import Optional, Dict, Any, Union


BASE_URL = "https://accounts.spotify.com"

async def get_access_token(client_id: str, client_secret: str, refresh_token: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """Получение нового Access token от Spotify с использованием Refresh token. (POST /api/token)

    Args:
        client_id (str): Идентификатор клиента Spotify
        client_secret (str): Секретный ключ клиента Spotify
        refresh_token (str): Refresh токен для получения нового Access token

    Returns:
        (Union[Dict[str, Any], Dict[str, str]]): Ответ от Spotify с новым Access token или ошибкой
    """
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_creds_b64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.post(url="/api/token", headers=headers, data=data)
        except httpx.RequestError as e:
            return {
                "python_error": "request_error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "python_error": "unexpected_error",
                "message": str(e)
            }
        if response.status_code != 200:
            return response.json()
        return response.json()



    