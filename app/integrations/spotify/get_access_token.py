import base64
from typing import Any, Dict

import httpx

BASE_URL = "https://accounts.spotify.com"


async def get_access_token(
    client_id: str, client_secret: str, refresh_token: str
) -> Dict[str, Any]:
    """
    Получение нового Access token от Spotify с использованием Refresh token. (POST /api/token)

    :param client_id: Идентификатор клиента Spotify
    :type client_id: str
    :param client_secret: Секретный ключ клиента Spotify
    :type client_secret: str
    :param refresh_token: Refresh токен для получения нового Access token
    :type refresh_token: str
    :return: Ответ от Spotify с новым Access token или ошибкой

        В случае ошибки Python возвращает словарь с ключами:
            - **python_error** (str): Тип ошибки Python ("request_error" или "unexpected_error").
            - **message** (str): Описание ошибки Python.
    :rtype: Dict[str, Any]
    """

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_creds_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.post(url="/api/token", headers=headers, data=data)
        except httpx.RequestError as e:
            return {"python_error": "request_error", "message": str(e)}
        except Exception as e:
            return {"python_error": "unexpected_error", "message": str(e)}
        return response.json()
