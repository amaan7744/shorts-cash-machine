import random, yaml
from moviepy.editor import VideoFileClip

def extract_clip(path):
    cfg = yaml.safe_load(open("config.yaml"))
    v = VideoFileClip(path)

    start = random.uniform(0, max(0, v.duration - cfg["shorts"]["clip_max_seconds"]))
    dur = random.uniform(cfg["shorts"]["clip_min_seconds"], cfg["shorts"]["clip_max_seconds"])

    out = "data/clip.mp4"
    v.subclip(start, start + dur).write_videofile(
        out, codec="libx264", audio_codec="aac", verbose=False, logger=None
    )
    return out
