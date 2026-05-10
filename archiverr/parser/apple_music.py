from pathlib import Path
import plistlib

from archiverr.core.models import Track



def parse_library(path: str):
    path = Path(path)

    with open(path, "rb") as f:
        data = plistlib.load(f)

    tracks = []

    for _, item in data.get("Tracks", {}).items():
        tracks.append(
            Track(
                title=item.get("Name", "Unknown"),
                artist=item.get("Artist", "Unknown"),
                album=item.get("Album"),
                year=item.get("Year"),
                duration_ms=item.get("Total Time"),
            )
        )

    return tracks
