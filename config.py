from pathlib import Path

MAX_SHORTS_PER_DAY = 3
MIN_CLIP_LEN = 7
MAX_CLIP_LEN = 25

TEMP_DIR = Path("temp")
VIDEO_DIR = TEMP_DIR / "videos"
CLIP_DIR = TEMP_DIR / "clips"
AUDIO_DIR = TEMP_DIR / "audio"
SUB_DIR = TEMP_DIR / "subs"

OUTPUT_DIR = Path("output/shorts")

for d in [VIDEO_DIR, CLIP_DIR, AUDIO_DIR, SUB_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)
