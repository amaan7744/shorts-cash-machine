from fetch import download_video
from audio_detect import detect_spikes
from clipper import extract_clips
from subtitles import transcribe_clip
from vertical import make_vertical
from config import MAX_SHORTS_PER_DAY
from logger import logger
from pathlib import Path

def run(channel_video_url):
    if not download_video(channel_video_url):
        return

    video = next(Path("temp/videos").glob("*.mp4"))
    spikes = detect_spikes(video)

    clips = extract_clips(video, spikes)

    shorts_done = 0
    for clip in clips:
        if shorts_done >= MAX_SHORTS_PER_DAY:
            break

        srt = transcribe_clip(clip)
        if not srt:
            continue

        out = make_vertical(clip, srt)
        if out:
            shorts_done += 1

    logger.info(f"Generated {shorts_done} shorts")

if __name__ == "__main__":
    run("PASTE_YOUTUBE_VIDEO_URL")
