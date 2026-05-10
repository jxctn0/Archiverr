import os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyEngine:
    def __init__(self):
        self.client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            )
        )

    def resolve(self, track):
        query = f"track:{track.title} artist:{track.artist}"

        results = self.client.search(q=query, type="track", limit=1)

        items = results.get("tracks", {}).get("items", [])

        if not items:
            return None

        item = items[0]

        return {
            "spotify_id": item["id"],
            "isrc": item["external_ids"].get("isrc"),
        }
