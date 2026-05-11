import os
import random
import sqlite3

from archiverr.database.db import Database
from archiverr.parser.apple_music import parse_library


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

    # insert batches (simplified)
    conn.execute(
        "INSERT INTO ingest_batches (batch_id, source_file) VALUES (?, ?)",
        ("test_batch", LIBRARY_PATH),
    )

    # insert tracks
    for track in library.tracks.values():
        conn.execute(
    """
    INSERT INTO raw_tracks (
        import_batch_id,
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
        raw_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "test_batch",
        track.title,
        track.artist,
        track.album,
        track.album_artist,
        track.composer,
        track.genre,
        track.year,
        str(track.release_date) if track.release_date else None,
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
        str(track.raw_apple_data),
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
        assert t["artist"], "Missing artist"

    # -------------------------
    # PLAYLIST TESTS
    # -------------------------
    playlists = conn.execute("SELECT * FROM playlists").fetchall()

    if len(playlists) < 5:
        print("\n⚠️ Not enough playlists to sample (skipping strict test)")
    else:
        sample_playlists = random.sample(playlists, 5)

        print("\n📂 Random Playlist Samples:")
        for p in sample_playlists:
            print(f"- {p['name']}")
            assert p["name"], "Missing playlist name"

    print("\n✅ Random sampling DB test passed")


if __name__ == "__main__":
    test_random_tracks_and_playlists()