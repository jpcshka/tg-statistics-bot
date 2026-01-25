import base64
from typing import Any, Dict

import httpx

BASE_URL = "https://wakatime.com/api/v1"


async def get_daily_stats(wakatime_token: str) -> Dict[str, Any]:
    """
    Статиска за день на момент запроса. (GET /users/current/status_bar/today)

    :param wakatime_token: Токен для доступа к API Wakatime
    :type wakatime_token: str
    :return: Словарь со статистикой за день: дата, общее время, проекты, языки.

        В случае ошибки возвращает словарь с ключами:
            - **python_error** (str): Тип ошибки ("request_error" или "unexpected_error").
            - **message** (str): Описание ошибки.

        Или JSON ответ от Wakatime API при HTTP статусе != 200.
    :rtype: Dict[str, Any]
    """

    token = base64.b64encode(wakatime_token.encode()).decode()

    headers = {"Authorization": f"Basic {token}"}
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.get(
                url="/users/current/status_bar/today", headers=headers
            )
        except httpx.RequestError as e:
            return {"python_error": "request_error", "message": str(e)}
        except Exception as e:
            return {"python_error": "unexpected_error", "message": str(e)}
        if response.status_code != 200:
            return response.json()
        data = response.json()
        result = {
            "date": data.get("cached_at"),
            "total": data.get("data").get("grand_total"),
            "projects": data.get("data").get("projects"),
            "languages": data.get("data").get("languages"),
        }
        return result


async def get_stats_for_range(
    wakatime_token: str, start: str, end: str
) -> Dict[str, Any]:
    """
    Статистика за указанный диапазон дат. (GET /users/current/summaries)

    :param wakatime_token: Токен для доступа к API Wakatime
    :type wakatime_token: str
    :param start: Начальная дата в формате 'YYYY-MM-DD'
    :type start: str
    :param end: Конечная дата в формате 'YYYY-MM-DD'
    :type end: str
    :return: Статистика за указанный диапазон дат: общее время, среднее за диапазон и данные по дням.

        В случае ошибки возвращает словарь с ключами:
            - **python_error** (str): Тип ошибки ("request_error" или "unexpected_error").
            - **message** (str): Описание ошибки.

        Или JSON ответ от Wakatime API при HTTP статусе != 200.
    :rtype: Dict[str, Any]
    """

    token = base64.b64encode(wakatime_token.encode()).decode()
    headers = {"Authorization": f"Basic {token}"}

    params = {"start": start, "end": end}
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.get(
                url="/users/current/summaries", headers=headers, params=params
            )
        except httpx.RequestError as e:
            return {"python_error": "request_error", "message": str(e)}
        except Exception as e:
            return {"python_error": "unexpected_error", "message": str(e)}
        if response.status_code != 200:
            return response.json()
        data = response.json()
        result = {
            "total": data.get("cumulative_total"),
            "average": data.get("daily_average"),
            "days": data.get("data"),
        }
        return result
