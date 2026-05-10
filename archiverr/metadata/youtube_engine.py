import yt_dlp


class YouTubeEngine:
    def resolve(self, track):
        query = f"{track.artist} - {track.title} official audio"

        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            result = ydl.extract_info(
                f"ytsearch1:{query}",
                download=False,
            )

        entries = result.get("entries", [])

        if not entries:
            return None

        entry = entries[0]

        return {
            "youtube_id": entry["id"],
            "youtube_url": f"https://youtube.com/watch?v={entry['id']}"
        }
