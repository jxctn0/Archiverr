import asyncio
import musicbrainzngs


musicbrainzngs.set_useragent(
    "Archiverr",
    "1.0",
    "https://github.com/jxctn0/archiverr",
)


class MusicBrainzEngine:
    async def resolve(self, track):
        await asyncio.sleep(1)

        result = musicbrainzngs.search_recordings(
            recording=track.title,
            artist=track.artist,
            limit=1,
        )

        recordings = result.get("recording-list", [])

        if not recordings:
            return None

        return recordings[0]
