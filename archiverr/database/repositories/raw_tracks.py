import json
from datetime import datetime
from typing import Dict, Any, Iterable

from archiverr.database.db import Database


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
                    track.track_id,
                    track.persistent_id,
                    track.title,
                    track.artist,
                    track.album,
                    track.album_artist,
                    track.composer,
                    track.genre,
                    track.year,
                    track.release_date.isoformat() if track.release_date else None,
                    track.duration_ms,
                    track.track_number,
                    track.track_count,
                    track.disc_number,
                    track.disc_count,
                    track.kind,
                    track.size,
                    track.bitrate,
                    track.sample_rate,
                    track.location,
                    track.track_type,
                    int(track.protected),
                    int(track.apple_music),
                    json.dumps(track.raw_apple_data or {}),
                    batch_id,
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
                        json.dumps(t.raw_apple_data or {}),
                        batch_id,
                    )
                    for t in tracks
                ],
            )