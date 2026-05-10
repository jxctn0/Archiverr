from dataclasses import dataclass
from typing import Optional


@dataclass
class Track:
    title: str
    artist: str

    album: Optional[str] = None
    year: Optional[int] = None
    duration_ms: Optional[int] = None

    canonical_id: Optional[str] = None
    isrc: Optional[str] = None

    spotify_id: Optional[str] = None
    musicbrainz_id: Optional[str] = None
    youtube_id: Optional[str] = None

    youtube_url: Optional[str] = None
    local_path: Optional[str] = None
