import subprocess
from pathlib import Path
from logger import logger
import uuid

def prepend_audio(video_path: Path, hook_audio: Path) -> Path:
    """
    Prepends hook_audio before original video audio.
    Returns new video path.
    """
    out = Path("temp/clips") / f"merged_{uuid.uuid4()}.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(hook_audio),
        "-i", str(video_path),
        "-filter_complex",
        "[0:a][1:a]concat=n=2:v=0:a=1[a]",
        "-map", "1:v",
        "-map", "[a]",
        "-c:v", "copy",
        str(out)
    ]

    try:
        subprocess.run(cmd, check=True)
        return out
    except Exception as e:
        logger.warning(f"Audio merge failed, using original clip: {e}")
        return video_path
