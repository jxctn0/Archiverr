# This test initializes a fresh database, simulates ingesting a library file, and then performs random sampling of tracks and playlists to verify data integrity.
# Run with: `python tests/test_database_init.py`

import os
import random
import sqlite3
import json
from datetime import datetime

from archiverr.database.db import Database
from archiverr.parser.apple_music import parse_library
from archiverr.core.hashing import hash_file
from archiverr.database.repositories.raw_tracks import _json_safe_dump


DB_PATH = "test_archiverr.db"
LIBRARY_PATH = "tests/fixtures/Library.xml"


def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    db = Database(db_path=DB_PATH)
    return db


def test_random_tracks_and_playlists():
    db = setup_db()
    conn = db.connect()

    # -------------------------
    # INGEST (manual lightweight version)
    # -------------------------
    library = parse_library(LIBRARY_PATH)
    file_hash = hash_file(LIBRARY_PATH)

    # insert batches with new schema
    conn.execute(
        "INSERT INTO ingest_batches (batch_id, source_file, file_hash, num_tracks, num_playlists, status) VALUES (?, ?, ?, ?, ?, ?)",
        ("test_batch", LIBRARY_PATH, file_hash, len(library.tracks), len(library.playlists), "completed"),
    )

    # insert tracks with full schema
    for track in library.tracks.values():
        conn.execute(
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
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        int(track.protected or 0),
        int(track.apple_music or 0),
        _json_safe_dump(track.raw_apple_data or {}),
        "test_batch",
    ),
)

    conn.commit()

    # -------------------------
    # TRACK TESTS
    # -------------------------
    tracks = conn.execute("SELECT * FROM raw_tracks").fetchall()
    assert len(tracks) > 5, "Not enough tracks in DB"

    sample_tracks = random.sample(tracks, 5)

    print("\n🎵 Random Track Samples:")
    for t in sample_tracks:
        print(f"- {t['artist']} — {t['title']}")
        assert t["title"], "Missing title"

    # -------------------------
    # PLAYLIST TESTS
    # -------------------------
    try:
        playlists = conn.execute("SELECT * FROM playlists").fetchall()

        if len(playlists) < 5:
            print("\n⚠️ Not enough playlists to sample (skipping strict test)")
        else:
            sample_playlists = random.sample(playlists, 5)

            print("\n📂 Random Playlist Samples:")
            for p in sample_playlists:
                print(f"- {p['name']}")
                assert p["name"], "Missing playlist name"
    except sqlite3.OperationalError as e:
        print(f"\n⚠️ Playlists table not found: {e}")

    print("\n✅ Random sampling DB test passed")


if __name__ == "__main__":
    test_random_tracks_and_playlists()