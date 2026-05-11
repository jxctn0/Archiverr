-- =========================================
-- ARCHIVERR DATABASE SCHEMA
-- RAW → CANONICAL → RESOLUTION → DOWNLOAD
-- =========================================

PRAGMA foreign_keys = ON;

-- =========================================
-- 0. METADATA VERSIONING
-- =========================================

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY
);

INSERT OR IGNORE INTO schema_version (version) VALUES (1);

-- =========================================
-- 1. INGESTION BATCH TRACKING
-- =========================================

CREATE TABLE IF NOT EXISTS ingest_batches (
    batch_id TEXT PRIMARY KEY,

    source_file TEXT,
    file_hash TEXT UNIQUE,

    total_tracks INTEGER DEFAULT 0,
    num_tracks INTEGER DEFAULT 0,
    num_playlists INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',

    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 2. RAW TRACKS (IMMUTABLE SOURCE LAYER)
-- =========================================

CREATE TABLE IF NOT EXISTS raw_tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Apple identifiers
    track_id INTEGER,
    persistent_id TEXT,

    -- Core metadata
    title TEXT,
    artist TEXT,
    album TEXT,
    album_artist TEXT,
    composer TEXT,
    genre TEXT,
    year INTEGER,
    release_date TEXT,

    duration_ms INTEGER,
    track_number INTEGER,
    track_count INTEGER,
    disc_number INTEGER,
    disc_count INTEGER,

    -- File metadata
    kind TEXT,
    size INTEGER,
    bitrate INTEGER,
    sample_rate INTEGER,
    location TEXT,
    track_type TEXT,

    -- Flags
    protected INTEGER DEFAULT 0,
    apple_music INTEGER DEFAULT 0,

    -- Full original Apple payload (future-proofing)
    raw_json TEXT,

    -- ingestion metadata
    import_batch_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (import_batch_id)
    REFERENCES ingest_batches(batch_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_raw_tracks_track_id ON raw_tracks(track_id);
CREATE INDEX IF NOT EXISTS idx_raw_tracks_persistent_id ON raw_tracks(persistent_id);
CREATE INDEX IF NOT EXISTS idx_raw_tracks_artist ON raw_tracks(artist);
CREATE INDEX IF NOT EXISTS idx_raw_tracks_title ON raw_tracks(title);
CREATE INDEX IF NOT EXISTS idx_raw_tracks_batch ON raw_tracks(import_batch_id);

-- Prevent duplicate raw inserts
CREATE UNIQUE INDEX IF NOT EXISTS idx_raw_unique_track
ON raw_tracks(track_id, persistent_id);

-- =========================================
-- 3. CANONICAL TRACKS (DEDUPED IDENTITY)
-- =========================================

CREATE TABLE IF NOT EXISTS canonical_tracks (
    canonical_id TEXT PRIMARY KEY,

    title TEXT,
    artist TEXT,
    album TEXT,

    duration_ms INTEGER,

    -- External identifiers
    isrc TEXT,
    spotify_id TEXT,
    musicbrainz_id TEXT,
    youtube_id TEXT,

    -- Best source pointer
    best_raw_id INTEGER,

    -- confidence scoring (0.0 - 1.0)
    confidence REAL DEFAULT 0.0,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (best_raw_id)
    REFERENCES raw_tracks(id)
    ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_canonical_artist ON canonical_tracks(artist);
CREATE INDEX IF NOT EXISTS idx_canonical_title ON canonical_tracks(title);
CREATE INDEX IF NOT EXISTS idx_canonical_isrc ON canonical_tracks(isrc);

-- Auto-update timestamp
CREATE TRIGGER IF NOT EXISTS update_canonical_updated_at
AFTER UPDATE ON canonical_tracks
BEGIN
    UPDATE canonical_tracks
    SET updated_at = CURRENT_TIMESTAMP
    WHERE canonical_id = NEW.canonical_id;
END;

-- =========================================
-- 4. RAW → CANONICAL MAPPING
-- =========================================

CREATE TABLE IF NOT EXISTS track_mapping (
    raw_id INTEGER,
    canonical_id TEXT,

    PRIMARY KEY (raw_id, canonical_id),

    FOREIGN KEY (raw_id)
    REFERENCES raw_tracks(id)
    ON DELETE CASCADE,

    FOREIGN KEY (canonical_id)
    REFERENCES canonical_tracks(canonical_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_mapping_canonical ON track_mapping(canonical_id);

-- =========================================
-- 5. EXTERNAL IDS (NORMALISED IDENTITY LAYER)
-- =========================================

CREATE TABLE IF NOT EXISTS external_ids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    canonical_id TEXT,

    source TEXT, -- spotify | musicbrainz | youtube | apple
    external_id TEXT,

    confidence REAL DEFAULT 0.0,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (canonical_id)
    REFERENCES canonical_tracks(canonical_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_external_ids_canonical ON external_ids(canonical_id);
CREATE INDEX IF NOT EXISTS idx_external_ids_source ON external_ids(source);

-- =========================================
-- 6. METADATA CACHE (API RATE LIMIT PROTECTION)
-- =========================================

CREATE TABLE IF NOT EXISTS metadata_cache (
    query_hash TEXT PRIMARY KEY,

    source TEXT,  -- spotify | musicbrainz | youtube
    query TEXT,

    result_json TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_cache_source ON metadata_cache(source);

-- =========================================
-- 7. DOWNLOAD TRACKING
-- =========================================

CREATE TABLE IF NOT EXISTS downloads (
    canonical_id TEXT PRIMARY KEY,

    file_path TEXT,
    file_extension TEXT,

    sha256 TEXT,
    blake3 TEXT,

    status TEXT DEFAULT 'pending',
    -- pending | downloading | done | failed | skipped

    source TEXT, -- youtube | spotify | local

    download_attempts INTEGER DEFAULT 0,

    last_error TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (canonical_id)
    REFERENCES canonical_tracks(canonical_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_download_status ON downloads(status);

-- =========================================
-- 8. RESOLUTION LOG (DEBUGGING + AUDIT)
-- =========================================

CREATE TABLE IF NOT EXISTS resolution_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    canonical_id TEXT,

    source TEXT, -- spotify | musicbrainz | youtube

    status TEXT, -- success | failed | partial

    confidence REAL,

    payload_json TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_resolution_canonical ON resolution_log(canonical_id);

-- =========================================
-- 9. ARTWORK CACHE
-- =========================================

CREATE TABLE IF NOT EXISTS artwork_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    canonical_id TEXT,

    url TEXT,
    local_path TEXT,

    source TEXT, -- spotify | musicbrainz | apple

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (canonical_id)
    REFERENCES canonical_tracks(canonical_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_artwork_canonical ON artwork_cache(canonical_id);