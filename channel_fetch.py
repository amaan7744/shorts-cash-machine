import subprocess
import json
from logger import logger


def get_latest_video_url(channel_url: str) -> str | None:
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
            return None

        latest = entries[0]

        # THIS IS THE FIX
        if "url" in latest:
            return latest["url"]

        # fallback
        video_id = latest.get("id")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

        return None

    except Exception as e:
        logger.error(f"Channel fetch failed: {e}")
        return None
