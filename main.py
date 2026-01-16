#!/usr/bin/env python3
import sys
import os
from pathlib import Path

from logger import logger
from config import (
    VIDEO_DIR,
    CLIP_DIR,
    OUTPUT_DIR,
    MAX_SHORTS_PER_DAY,
)

from fetch import download_video
from audio_detect import detect_spikes
from clipper import extract_clips
from subtitles import transcribe_clip
from vertical import make_vertical
from script_hook import generate_hook_script
from tts_generate import generate_hook
from video_merge import prepend_audio


def get_latest_video() -> Path | None:
    videos = sorted(VIDEO_DIR.glob("*.mp4"), key=os.path.getmtime)
    return videos[-1] if videos else None


def run(video_url: str):
    logger.info("===== SHORTS PIPELINE START =====")

    # --------------------------------------------------
    # 1. DOWNLOAD VIDEO
    # --------------------------------------------------
    logger.info("Downloading source video")
    if not download_video(video_url):
        logger.error("Download failed — exiting safely")
        return

    video_path = get_latest_video()
    if not video_path:
        logger.error("No downloaded video found — exiting")
        return

    logger.info(f"Using video: {video_path.name}")

    # --------------------------------------------------
    # 2. DETECT CHAOS MOMENTS
    # --------------------------------------------------
    spikes = detect_spikes(video_path)
    if not spikes:
        logger.warning("No spikes detected — exiting")
        return

    # --------------------------------------------------
    # 3. EXTRACT CLIPS (RAW)
    # --------------------------------------------------
    clips = extract_clips(video_path, spikes)
    if not clips:
        logger.warning("No usable clips extracted — exiting")
        return

    # HARD LIMIT — never exceed daily quota
    clips = clips[:MAX_SHORTS_PER_DAY]

    logger.info(f"Processing {len(clips)} clips (max allowed)")

    # --------------------------------------------------
    # 4. PROCESS EACH CLIP
    # --------------------------------------------------
    shorts_done = 0

    for idx, clip in enumerate(clips, start=1):
        logger.info(f"--- Clip {idx} ---")

        working_clip = clip

        # 4.1 Generate hook script
        hook_text = generate_hook_script()
        logger.info(f"Hook script: {hook_text}")

        # 4.2 Generate hook audio (voice cloned)
        hook_audio = generate_hook(hook_text)

        # 4.3 Prepend hook audio if available
        if hook_audio:
            logger.info("Prepending hook audio")
            working_clip = prepend_audio(clip, hook_audio)
        else:
            logger.info("Skipping hook audio (none generated)")

        # 4.4 Transcribe clip (for subtitles)
        srt = transcribe_clip(working_clip)
        if not srt:
            logger.warning("Subtitle generation failed — skipping clip")
            continue

        # 4.5 Render vertical short
        final_short = make_vertical(working_clip, srt)
        if not final_short:
            logger.warning("Final render failed — skipping clip")
            continue

        shorts_done += 1
        logger.info(f"Short created: {final_short.name}")

        if shorts_done >= MAX_SHORTS_PER_DAY:
            break

    # --------------------------------------------------
    # DONE
    # --------------------------------------------------
    logger.info(f"===== PIPELINE COMPLETE ({shorts_done} shorts) =====")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <YOUTUBE_VIDEO_URL>")
        sys.exit(1)

    run(sys.argv[1])
