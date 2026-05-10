import yt_dlp


class YTDLPEngine:
    def download(self, track, output_path):
        options = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([track.youtube_url])
