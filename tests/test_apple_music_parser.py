import random
from dataclasses import asdict
import json

from archiverr.parser.apple_music import parse_library


if __name__ == "__main__":
    library = parse_library("tests/fixtures/Library.xml")

    tracks = list(library.tracks.values())

    print(f"Imported {len(tracks)} tracks from large library")

    randnum = random.randint(0, len(tracks) - 5)

    print(f"Printing tracks from index {randnum} to {randnum + 5} to verify data")

    for track in tracks[randnum:randnum + 5]:
        print(json.dumps(asdict(track), indent=4, default=str))

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

    print(f"Protected tracks: {protected_tracks}")
    print(f"Apple Music tracks: {apple_music_tracks}")
    print(f"Tracks with missing locations: {missing_locations}")

    # Verify playlists are imported correctly
    print(f"Imported {len(library.playlists)} playlists from large library")
    for playlist in library.playlists[:100]: #
        # Print {playlist name} and number of tracks in the playlist
        print(f"Playlist: {playlist.name}, Number of tracks: {len(playlist.playlist_items)}")