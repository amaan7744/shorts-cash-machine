import subprocess
from logger import logger
from config import OUTPUT_DIR
import uuid

def make_vertical(video_path, srt_path):
    out = OUTPUT_DIR / f"{uuid.uuid4()}.mp4"

    vf = (
        "crop=ih*9/16:ih,"
        "scale=1080:1920,"
        "subtitles=" + str(srt_path)
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", vf,
        "-preset", "veryfast",
        "-c:a", "aac",
        str(out)
    ]

    try:
        subprocess.run(cmd, check=True)
        logger.info("Vertical short created")
        return out
    except Exception as e:
        logger.error(f"Vertical failed: {e}")
        return None
