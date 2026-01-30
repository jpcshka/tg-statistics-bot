from app.core.config import (
    REFRESH_TOKEN,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    DB_PATH,
)
from app.integrations.spotify.get_access_token import get_access_token
from app.integrations.spotify.get_track_history import get_track_history
from app.db.sessions import get_db
from app.db.sync_after import get_after, update_after
from app.db.spotify.write import (
    save_album,
    save_artist,
    save_playback,
    save_track,
    save_track_artist_relation,
)


async def collect_spotify_data() -> None:
    """Собирает данные из Spotify и сохраняет их в базу данных."""
    access_token_data = await get_access_token(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN,
    )
    access_token = access_token_data.get("access_token")
    if not access_token:
        raise ValueError("Не удалось получить access token")

    after = await get_after()

    track_history = await get_track_history(
        access_token=access_token, limit=30, after=after
    )

    new_after = track_history.get("after")
    if new_after:
        try:
            new_after_int = int(new_after)
            await update_after(new_after_int)
        except ValueError:
            print(f"Не удалось преобразовать after в int: {new_after}")

    if not DB_PATH:
        raise ValueError("DB_PATH не задан в .env")

    async with get_db() as db:
        for track in track_history.get("tracks", []):
            await save_track(db, track)
            await save_album(db, track.get("album", {}))
            for artist in track.get("artists", []):
                await save_artist(db, artist)
                await save_track_artist_relation(
                    db, track.get("track_id"), artist.get("artist_id")
                )
            await save_playback(db, track)
        await db.commit()
    print("Данные Spotify собраны и сохранены в базу данных.")
