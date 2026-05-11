import json
from datetime import datetime
from typing import Dict, Any, Iterable

from archiverr.database.db import Database


def _json_safe_dump(obj: Any) -> str:
    """Serialize complex Apple Music payloads into JSON-safe strings."""

    def _convert(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: _convert(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_convert(v) for v in value]
        if isinstance(value, tuple):
            return [_convert(v) for v in value]
        if isinstance(value, set):
            return [_convert(v) for v in value]
        return value

    return json.dumps(_convert(obj))


class RawTrackRepository:
    def __init__(self, db: Database):
        self.db = db

    def insert(self, track, batch_id: str) -> int:
        """
        Inserts a raw Apple Music track.
        Returns DB row ID.
        """

        with self.db.session() as conn:
            cursor = conn.execute(
                """
                INSERT INTO raw_tracks (
                    track_id,
                    persistent_id,
                    title,
                    artist,
                    album,
                    album_artist,
                    composer,
                    genre,
                    year,
                    release_date,
                    duration_ms,
                    track_number,
                    track_count,
                    disc_number,
                    disc_count,
                    kind,
                    size,
                    bitrate,
                    sample_rate,
                    location,
                    track_type,
                    protected,
                    apple_music,
                    raw_json,
                    import_batch_id
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    track.track_id, # Type: Optional[int]
                    track.persistent_id, # Type: Optional[str]
                    track.title, # Type: Optional[str]
                    track.artist, # Type: Optional[str]
                    track.album, # Type: Optional[str]
                    track.album_artist, # Type: Optional[str]
                    track.composer, # Type: Optional[str]
                    track.genre, # Type: Optional[str]
                    track.year,  # Type: Optional[int]
                    track.release_date.isoformat() if track.release_date else None, # Type: Optional[datetime]
                    track.duration_ms, # Type: Optional[int]
                    track.track_number, # Type: Optional[int]
                    track.track_count, # Type: Optional[int]
                    track.disc_number, # Type: Optional[int]
                    track.disc_count, # Type: Optional[int]
                    track.kind, # Type: Optional[str]
                    track.size, # Type: Optional[int]
                    track.bitrate, # Type: Optional[int]
                    track.sample_rate, # Type: Optional[int]
                    track.location, # Type: Optional[str]
                    track.track_type, # Type: Optional[str]
                    int(track.protected), # Type: Optional[bool] -> int
                    int(track.apple_music), # Type: Optional[bool] -> int
                    _json_safe_dump(track.raw_apple_data or {}), # Type: Optional[Dict[str, Any]] -> str
                    batch_id, # Type: str
                ),
            )

            return cursor.lastrowid

    def bulk_insert(self, tracks: Iterable, batch_id: str):
        """
        Fast batch ingestion (future optimization point).
        """
        with self.db.session() as conn:
            conn.executemany(
                """
                INSERT INTO raw_tracks (
                    track_id, persistent_id, title, artist, album,
                    album_artist, composer, genre, year, release_date,
                    duration_ms, track_number, track_count,
                    disc_number, disc_count, kind, size, bitrate,
                    sample_rate, location, track_type,
                    protected, apple_music, raw_json, import_batch_id
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                [
                    (
                        t.track_id,
                        t.persistent_id,
                        t.title,
                        t.artist,
                        t.album,
                        t.album_artist,
                        t.composer,
                        t.genre,
                        t.year,
                        t.release_date.isoformat() if t.release_date else None,
                        t.duration_ms,
                        t.track_number,
                        t.track_count,
                        t.disc_number,
                        t.disc_count,
                        t.kind,
                        t.size,
                        t.bitrate,
                        t.sample_rate,
                        t.location,
                        t.track_type,
                        int(t.protected),
                        int(t.apple_music),
                        _json_safe_dump(t.raw_apple_data or {}),
                        batch_id,
                    )
                    for t in tracks
                ],
            )