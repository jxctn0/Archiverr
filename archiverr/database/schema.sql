CREATE TABLE IF NOT EXISTS tracks (
    canonical_id TEXT PRIMARY KEY,
    title TEXT,
    artist TEXT,
    album TEXT,
    year INTEGER,
    isrc TEXT,
    spotify_id TEXT,
    musicbrainz_id TEXT,
    youtube_id TEXT,
    youtube_url TEXT,
    local_path TEXT
);
