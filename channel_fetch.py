import subprocess
import json
from logger import logger


def get_latest_video_url(channel_url: str) -> str | None:
    """
    Fetches the latest video URL from a YouTube channel
    using yt-dlp (no API keys, CI-safe).
    """
    try:
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--dump-single-json",
            channel_url
        ]

        output = subprocess.check_output(cmd, text=True)
        data = json.loads(output)

        entries = data.get("entries", [])
        if not entries:
            logger.error("No videos found on channel")
            return None

        latest = entries[0]
        video_id = latest.get("id")

        if not video_id:
            logger.error("Latest video ID missing")
            return None

        return f"https://www.youtube.com/watch?v={video_id}"

    except Exception as e:
        logger.error(f"Failed to fetch latest video: {e}")
        return None
