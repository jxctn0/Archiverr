############ test_apple_music_parser.py ###############
#
# Test helper script for Apple Music library parsing.
# Loads the sample library fixture and prints summary information
# for tracks and playlists to help verify parser output.
#
#=======================================================

import random
from dataclasses import asdict
import json

from archiverr.parser.apple_music import parse_library
from archiverr.core.logging import log # Custom logging module with color-coded output


if __name__ == "__main__":
    library = parse_library("tests/fixtures/Library.xml")

    tracks = list(library.tracks.values())

    log(f"Imported {len(tracks)} tracks from large library") # Print the total number of tracks imported from the library to verify that the parser is correctly reading the track data from the XML file

    randnum = random.randint(0, len(tracks) - 5)

    log(f"Printing tracks from index {randnum} to {randnum + 5} to verify data")

    for track in tracks[randnum:randnum + 5]:
        # Print the track title, artist, album, and duration in a human-readable format
        log(f"Title: {track.title}, Artist: {track.artist}, Album: {track.album}, Duration: {track.duration_ms} ms")
        log(track, level="debug") # Log the full track data as a dictionary for debugging purposes

    # Verify different fields are populated correctly
    protected_tracks = 0
    apple_music_tracks = 0
    missing_locations = 0

    for track in tracks:
        if track.protected:
            protected_tracks += 1

        if track.apple_music:
            apple_music_tracks += 1

        if not track.location:
            missing_locations += 1

    log(f"Protected tracks: {protected_tracks}")
    log(f"Apple Music tracks: {apple_music_tracks}")
    log(f"Tracks with missing locations: {missing_locations}")

    # Verify playlists are imported correctly
    log(f"Imported {len(library.playlists)} playlists from large library")
    for playlist in library.playlists[:100]: #
        # Print {playlist name} and number of tracks in the playlist
        log(f"Playlist: {playlist.name}, Number of tracks: {len(playlist.playlist_items)}")

    