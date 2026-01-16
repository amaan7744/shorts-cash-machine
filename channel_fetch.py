import subprocess
from logger import logger


def get_latest_video_url(channel_url: str) -> str | None:
    """
    Returns the URL of the latest video from a YouTube channel.
    This method is CI-safe and avoids channel-ID confusion.
    """
    try:
        cmd = [
            "yt-dlp",
            "--playlist-items", "1",
            "--print", "url",
            channel_url
        ]

        output = subprocess.check_output(cmd, text=True).strip()

        if not output.startswith("http"):
            logger.error(f"Invalid video URL returned: {output}")
            return None

        logger.info(f"Latest video resolved: {output}")
        return output

    except Exception as e:
        logger.error(f"Failed to resolve latest video: {e}")
        return None
