import aiosqlite


async def init_db(DB_PATH):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                    CREATE TABLE IF NOT EXISTS albums (
                        album_id TEXT PRIMARY KEY,
                        title TEXT, 
                        album_type TEXT,
                        release_date TEXT,
                        total_tracks INTEGER,
                        external_urls TEXT
                        );
                    """)

        await db.execute("""
                    CREATE TABLE IF NOT EXISTS artists (
                        artist_id TEXT PRIMARY KEY,
                        name TEXT,
                        type TEXT,
                        external_urls TEXT
                        );
                    """)

        await db.execute("""
                    CREATE TABLE IF NOT EXISTS tracks (
                        track_id TEXT PRIMARY KEY,
                        title TEXT, 
                        type TEXT,
                        album_id TEXT,
                        explicit TEXT,
                        duration_ms INTEGER,
                        external_urls TEXT,
                    
                        FOREIGN KEY (album_id) REFERENCES albums(album_id)
                        );
                    """)

        await db.execute("""
                    CREATE TABLE IF NOT EXISTS track_artists (
                        track_id TEXT,
                        artist_id TEXT,
                    
                        FOREIGN KEY (track_id) REFERENCES tracks(track_id),
                        FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
                    
                        PRIMARY KEY (track_id, artist_id)
                        );
                    """)

        await db.execute("""
                    CREATE TABLE IF NOT EXISTS played_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        track_id TEXT NOT NULL,
                        played_at TEXT NOT NULL,

                        FOREIGN KEY (track_id) REFERENCES tracks(track_id)
                        );
                    """)

        await db.commit()
