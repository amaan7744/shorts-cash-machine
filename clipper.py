import subprocess
from config import CLIP_DIR, MIN_CLIP_LEN, MAX_CLIP_LEN
from logger import logger
import uuid

def extract_clips(video_path, spikes):
    clips = []
    for start, end in spikes:
        dur = end - start
        if dur < MIN_CLIP_LEN or dur > MAX_CLIP_LEN:
            continue

        out = CLIP_DIR / f"{uuid.uuid4()}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-to", str(end),
            "-i", video_path,
            "-c", "copy",
            str(out)
        ]

        try:
            subprocess.run(cmd, check=True)
            clips.append(out)
        except:
            logger.warning("Clip skipped")

    return clips
