from pathlib import Path
import plistlib
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from archiverr.core.models import Track, Playlist, Library
#from archiverr.database import Database

# Example of the structure of the header of an Apple Music library XML file
# The actual file will contain many more fields and nested structures, but this is a simplified example to illustrate the parsing process


"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Major Version</key><integer>1</integer>
    <key>Minor Version</key><integer>1</integer>
    <key>Date</key><date>2026-05-06T23:12:25Z</date>
    <key>Application Version</key><string>1.5.6.11</string>
    <key>Features</key><integer>5</integer>
    <key>Show Content Ratings</key><true/>
    <key>Music Folder</key><string>file:///Users/user/Music/Music/Media.localized/</string>
    <key>Library Persistent ID</key><string>E23416E7222FA7C5</string>

    <key>Tracks</key>
"""



def parse_library(path: str):
    # Parse the Apple Music library XML file and return a Library object
    with open(path, "rb") as f:
        plist = plistlib.load(f)

    # Create a Library object from the parsed plist data
    library = Library(
        major_version=plist.get("Major Version", 1),
        minor_version=plist.get("Minor Version", 1),
        date=plist.get("Date"),
        application_version=plist.get("Application Version", ""),
        features=plist.get("Features", 5),
        show_content_ratings=plist.get("Show Content Ratings", True),
        music_folder=plist.get("Music Folder", ""),
        library_persistent_id=plist.get("Library Persistent ID", ""),
    )

    # Parse tracks
    tracks_dict = plist.get("Tracks", {})
    for track_id_str, track_data in tracks_dict.items():
        track_id = int(track_id_str)
        track = Track(
            title=track_data.get("Name", ""),
            artist=track_data.get("Artist", ""),
            album=track_data.get("Album"),
            album_artist=track_data.get("Album Artist"),
            composer=track_data.get("Composer"),
            genre=track_data.get("Genre"),
            year=track_data.get("Year"),
            release_date=track_data.get("Release Date"),
            duration_ms=track_data.get("Total Time"),
            track_number=track_data.get("Track Number"),
            track_count=track_data.get("Track Count"),
            disc_number=track_data.get("Disc Number"),
            disc_count=track_data.get("Disc Count"),
        )
        library.tracks[track_id] = track

    # Parse playlists
    playlists_list = plist.get("Playlists", [])
    for playlist_data in playlists_list:
        playlist = Playlist(
            name=playlist_data.get("Name", ""),
            description=playlist_data.get("Description"),
            playlist_id=playlist_data.get("Playlist ID", 0),
            playlist_persistent_id=playlist_data.get("Playlist Persistent ID", ""),
            all_items=playlist_data.get("All Items", True),
            playlist_items=playlist_data.get("Playlist Items", []),
        )
        library.playlists.append(playlist)

    return library