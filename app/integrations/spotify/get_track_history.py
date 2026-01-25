from typing import Any, Dict, Optional

import httpx

BASE_URL = "https://api.spotify.com/v1"


async def get_track_history(
    access_token: str, limit: Optional[int] = 50, after: Optional[int] = None
) -> Dict[str, Any]:
    """
    Делает запрос к Spotify API для получения истории прослушанных треков пользователя.
    (GET /me/player/recently-played)

    :param access_token: Токен доступа Spotify API.
    :type access_token: str
    :param limit: Количество треков для получения. По умолчанию 50 (максимум).
    :type limit: Optional[int]
    :param after: Временная метка (в миллисекундах) для получения треков, после этого времени.
        По умолчанию None.
    :type after: Optional[int]
    :return: Словарь с историей прослушанных треков или информацией об ошибке.

        В случае ошибки возвращает словарь с ключами:
            - **python_error** (str): Тип ошибки ("request_error" или "unexpected_error").
            - **message** (str): Описание ошибки.

        Или JSON ответ от Spotify API при HTTP статусе != 200.
    :rtype: Dict[str, Any]
    """

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": limit}

        if after is not None:
            params["after"] = after

        try:
            response = await client.get(
                "me/player/recently-played", headers=headers, params=params, timeout=15
            )
            # response.raise_for_status()
        except httpx.RequestError as e:
            # Network/timeout/DNS/etc.
            return {"python_error": "request_error", "message": str(e)}
        except Exception as e:
            # Any other unexpected Python-side error
            return {"python_error": "unexpected_error", "message": str(e)}
        if response.status_code != 200:
            return response.json()

        data = response.json()
        result = {
            "before": data.get("cursors", {}).get("before"),
            "after": data.get("cursors", {}).get("after"),
        }
        tracks = []
        for item in data.get("items", []):
            track_info = item.get("track", {})
            data = {
                "track_id": track_info.get("id"),
                "track_title": track_info.get("name"),
                "track_type": track_info.get("type"),
                "explicit": track_info.get("explicit"),
                "duration_ms": track_info.get("duration_ms"),
                "played_at": item.get("played_at"),
                "external_url": track_info.get("external_urls", {}).get("spotify"),
            }
            album_info = track_info.get("album", {})
            data["album"] = {
                "album_id": album_info.get("id"),
                "album_title": album_info.get("name"),
                "album_type": album_info.get("album_type"),
                "release_date": album_info.get("release_date"),
                "total_tracks": album_info.get("total_tracks"),
                "external_url": album_info.get("external_urls", {}).get("spotify"),
            }
            artists = []
            for artist in track_info.get("artists", []):
                artists.append(
                    {
                        "artist_id": artist.get("id"),
                        "artist_name": artist.get("name"),
                        "type": artist.get("type"),
                        "external_url": artist.get("external_urls", {}).get("spotify"),
                    }
                )
            data["artists"] = artists
            tracks.append(data)
        result["tracks"] = tracks
        return result
