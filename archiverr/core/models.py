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
    # --------------------------------------------------
    # Canonical Metadata
    # --------------------------------------------------

    title: str
    artist: str

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

    # --------------------------------------------------
    # Sorting Metadata
    # --------------------------------------------------

    sort_name: Optional[str] = None
    sort_artist: Optional[str] = None
    sort_album: Optional[str] = None

    # --------------------------------------------------
    # File Metadata
    # --------------------------------------------------

    kind: Optional[str] = None

    size: Optional[int] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None

    location: Optional[str] = None
    track_type: Optional[str] = None

    protected: bool = False
    apple_music: bool = False

    # --------------------------------------------------
    # Apple Metadata
    # --------------------------------------------------

    track_id: Optional[int] = None
    persistent_id: Optional[str] = None

    play_count: Optional[int] = None
    play_date: Optional[int] = None
    play_date_utc: Optional[datetime] = None

    date_added: Optional[datetime] = None
    date_modified: Optional[datetime] = None

    normalization: Optional[int] = None

    file_folder_count: Optional[int] = None
    library_folder_count: Optional[int] = None

    # --------------------------------------------------
    # External Metadata
    # --------------------------------------------------

    canonical_id: Optional[str] = None

    isrc: Optional[str] = None

    spotify_id: Optional[str] = None
    musicbrainz_id: Optional[str] = None
    youtube_id: Optional[str] = None

    youtube_url: Optional[str] = None

    # --------------------------------------------------
    # Local Archive Metadata
    # --------------------------------------------------

    local_path: Optional[str] = None

    sha256: Optional[str] = None
    blake3: Optional[str] = None

    acoustid: Optional[str] = None
    chromaprint: Optional[str] = None

    # --------------------------------------------------
    # Raw Metadata
    # --------------------------------------------------

    raw_apple_data: dict = field(default_factory=dict)

    # Return dict representation of the track for easier serialization and debugging
    def __dict__(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "album_artist": self.album_artist,
            "composer": self.composer,
            "genre": self.genre,
            "year": self.year,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "duration_ms": self.duration_ms,
            "track_number": self.track_number,
            "track_count": self.track_count,
            "disc_number": self.disc_number,
            "disc_count": self.disc_count,
            "sort_name": self.sort_name,
            "sort_artist": self.sort_artist,
            "sort_album": self.sort_album,
            "kind": self.kind,
            "size": self.size,
            "bitrate": self.bitrate,
            "sample_rate": self.sample_rate,
            "location": self.location,
            "track_type": self.track_type,
            "protected": self.protected,
            "apple_music": self.apple_music,
            "track_id": self.track_id,
            "persistent_id": self.persistent_id,
            "play_count": self.play_count,
            "play_date": datetime.utcfromtimestamp(self.play_date / 1000).isoformat() if self.play_date else None,
            "play_date_utc": self.play_date_utc.isoformat() if self.play_date_utc else None,
            "date_added": self.date_added.isoformat() if self.date_added else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,
            "normalization": self.normalization,
            "file_folder_count": self.file_folder_count,
            "library_folder_count": self.library_folder_count
        }
