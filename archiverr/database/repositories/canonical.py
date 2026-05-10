from archiverr.database.db import Database


class CanonicalRepository:
    def __init__(self, db: Database):
        self.db = db

    def insert_if_missing(self, canonical_id: str, track):
        with self.db.session() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO canonical_tracks (
                    canonical_id,
                    title,
                    artist,
                    album,
                    duration_ms,
                    isrc
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    canonical_id,
                    track.title,
                    track.artist,
                    track.album,
                    track.duration_ms,
                    getattr(track, "isrc", None),
                ),
            )

    def link_raw(self, raw_id: int, canonical_id: str):
        with self.db.session() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO track_mapping (
                    raw_id,
                    canonical_id
                )
                VALUES (?, ?)
                """,
                (raw_id, canonical_id),
            )