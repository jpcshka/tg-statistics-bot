import aiosqlite
from typing import Dict, Any


async def save_track(db: aiosqlite.Connection, track: Dict[str, Any]) -> None:
    """Сохраняет трек"""
    await db.execute(
        "INSERT OR IGNORE INTO tracks (track_id, title, type, album_id, explicit, duration_ms, external_urls) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            track["track_id"],
            track["track_title"],
            track["track_type"],
            track["album"].get("album_id"),
            track["explicit"],
            track["duration_ms"],
            track["external_url"],
        ),
    )


async def save_album(db: aiosqlite.Connection, album: Dict[str, Any]) -> None:
    """Сохраняет альбом"""
    await db.execute(
        "INSERT OR IGNORE INTO albums (album_id, title, album_type, release_date, total_tracks, external_urls) VALUES (?, ?, ?, ?, ?, ?)",
        (
            album["album_id"],
            album["album_title"],
            album["album_type"],
            album["release_date"],
            album["total_tracks"],
            album["external_url"],
        ),
    )


async def save_artist(db: aiosqlite.Connection, artist: Dict[str, str]) -> None:
    """Сохраняет артиста"""
    await db.execute(
        "INSERT OR IGNORE INTO artists (artist_id, name, type, external_urls) VALUES (?, ?, ?, ?)",
        (
            artist["artist_id"],
            artist["artist_name"],
            artist["type"],
            artist["external_url"],
        ),
    )


async def save_track_artist_relation(
    db: aiosqlite.Connection, track_id: str, artist_id: str
) -> None:
    """Сохраняет связь трека и артиста"""
    await db.execute(
        "INSERT OR IGNORE INTO track_artists (track_id, artist_id) VALUES (?, ?)",
        (
            track_id,
            artist_id,
        ),
    )


async def save_playback(db: aiosqlite.Connection, track: Dict[str, Any]) -> None:
    """Сохраняет воспроизведение"""
    await db.execute(
        "INSERT OR IGNORE INTO played_history (track_id, played_at) VALUES (?, ?)",
        (
            track["track_id"],
            track["played_at"],
        ),
    )
