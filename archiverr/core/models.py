from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Library:
    tracks: dict[int, Track] = field(default_factory=dict)
    playlists: list[Playlist] = field(default_factory=list)
    major_version: int = 1
    minor_version: int = 1
    date: Optional[datetime] = None
    application_version: str = ""
    features: int = 5
    show_content_ratings: bool = True
    music_folder: str = ""
    library_persistent_id: str = ""

    def __len__(self):
        return len(self.tracks)


@dataclass
class Playlist:
    name: str
    playlist_id: int
    playlist_persistent_id: str

    description: Optional[str] = None

    all_items: bool = True
    playlist_items: list = field(default_factory=list)

@dataclass
class Track:
    # =========================
    # REQUIRED CORE IDENTITY
    # =========================

    title: str
    artist: str

    # =========================
    # OPTIONAL MUSIC METADATA
    # =========================

    album: Optional[str] = None
    album_artist: Optional[str] = None
    composer: Optional[str] = None
    genre: Optional[str] = None

    year: Optional[int] = None
    release_date: Optional[datetime] = None

    duration_ms: Optional[int] = None

    track_number: Optional[int] = None
    track_count: Optional[int] = None
    disc_number: Optional[int] = None
    disc_count: Optional[int] = None

    # =========================
    # SORTING / DISPLAY METADATA
    # =========================

    sort_name: Optional[str] = None
    sort_artist: Optional[str] = None
    sort_album: Optional[str] = None

    # =========================
    # APPLE MUSIC METADATA
    # =========================

    track_id: Optional[int] = None
    persistent_id: Optional[str] = None

    play_count: Optional[int] = None
    play_date: Optional[int] = None
    play_date_utc: Optional[datetime] = None

    date_added: Optional[datetime] = None
    date_modified: Optional[datetime] = None

    normalization: Optional[int] = None

    protected: bool = False
    apple_music: bool = False

    kind: Optional[str] = None
    size: Optional[int] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None

    location: Optional[str] = None
    track_type: Optional[str] = None

    file_folder_count: Optional[int] = None
    library_folder_count: Optional[int] = None

    # =========================
    # RESOLUTION IDS
    # =========================

    canonical_id: Optional[str] = None

    isrc: Optional[str] = None

    spotify_id: Optional[str] = None
    musicbrainz_id: Optional[str] = None
    youtube_id: Optional[str] = None
    youtube_url: Optional[str] = None

    # =========================
    # LOCAL ARCHIVE DATA
    # =========================

    local_path: Optional[str] = None

    sha256: Optional[str] = None
    blake3: Optional[str] = None

    acoustid: Optional[str] = None
    chromaprint: Optional[str] = None

    # =========================
    # RAW SOURCE DATA
    # =========================

    raw_apple_data: dict = field(default_factory=dict)

    