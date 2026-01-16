import subprocess
from logger import logger
from config import VIDEO_DIR

def download_video(url: str) -> str | None:
    try:
        output = VIDEO_DIR / "%(id)s.%(ext)s"
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",
            "-o", str(output),
            url
        ]
        subprocess.run(cmd, check=True)
        logger.info("Downloaded video")
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return None
