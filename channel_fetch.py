import subprocess
from logger import logger


def normalize_channel_url(url: str) -> str:
    """
    Ensures we always point to the /videos tab,
    which yt-dlp can reliably process.
    """
    if "/videos" in url:
        return url
    return url.rstrip("/") + "/videos"


def get_latest_video_url(channel_url: str) -> str | None:
    """
    Returns the URL of the latest public video from a channel.
    Handles @handles safely for GitHub Actions.
    """
    try:
        channel_url = normalize_channel_url(channel_url)
        logger.info(f"Resolving channel videos page: {channel_url}")

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
