#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from logger import logger
from config import (
    VIDEO_DIR,
    MAX_SHORTS_PER_DAY,
)

from channel_manager import get_next_channel
from channel_fetch import get_latest_video_url
from fetch import download_video
from audio_detect import detect_spikes
from clipper import extract_clips
from script_hook import generate_hook_script
from tts_generate import generate_hook
from video_merge import prepend_audio
from subtitles import transcribe_clip
from vertical import make_vertical


def get_downloaded_video() -> Path | None:
    videos = sorted(VIDEO_DIR.glob("*.mp4"), key=os.path.getmtime)
    return videos[-1] if videos else None


def run_pipeline():
    logger.info("===== SHORTS PIPELINE START =====")

    # --------------------------------------------------
    # 1. SELECT CHANNEL (ROTATION)
    # --------------------------------------------------
    channel_url = get_next_channel()
    logger.info(f"Selected channel: {channel_url}")

    # --------------------------------------------------
    # 2. FETCH LATEST VIDEO
    # --------------------------------------------------
    video_url = get_latest_video_url(channel_url)
    if not video_url:
        logger.error("Failed to fetch latest video URL")
        return

    logger.info(f"Latest video URL: {video_url}")

    # --------------------------------------------------
    # 3. DOWNLOAD VIDEO
    # --------------------------------------------------
    if not download_video(video_url):
        logger.error("Video download failed")
        return

    video_path = get_downloaded_video()
    if not video_path:
        logger.error("Downloaded video not found")
        return

    logger.info(f"Downloaded video: {video_path.name}")

    # --------------------------------------------------
    # 4. DETECT CHAOS MOMENTS
    # --------------------------------------------------
    spikes = detect_spikes(video_path)
    if not spikes:
        logger.warning("No spikes detected")
        return

    # --------------------------------------------------
    # 5. EXTRACT CLIPS (HARD LIMIT)
    # --------------------------------------------------
    clips = extract_clips(video_path, spikes)
    if not clips:
        logger.warning("No clips extracted")
        return

    clips = clips[:MAX_SHORTS_PER_DAY]
    logger.info(f"Processing {len(clips)} clips")

    # --------------------------------------------------
    # 6. PROCESS EACH CLIP
    # --------------------------------------------------
    shorts_created = 0

    for i, clip in enumerate(clips, start=1):
        logger.info(f"--- Clip {i} ---")
        working_clip = clip

        # 6.1 Generate hook script
        hook_text = generate_hook_script()
        logger.info(f"Hook text: {hook_text}")

        # 6.2 Generate hook voice (cloned)
        hook_audio = generate_hook(hook_text)

        # 6.3 Prepend hook audio (optional)
        if hook_audio:
            working_clip = prepend_audio(clip, hook_audio)
        else:
            logger.info("No hook audio added")

        # 6.4 Generate subtitles
        srt = transcribe_clip(working_clip)
        if not srt:
            logger.warning("Subtitle generation failed, skipping clip")
            continue

        # 6.5 Render vertical short
        final_short = make_vertical(working_clip, srt)
        if not final_short:
            logger.warning("Final render failed, skipping clip")
            continue

        shorts_created += 1
        logger.info(f"Short created: {final_short.name}")

        if shorts_created >= MAX_SHORTS_PER_DAY:
            break

    logger.info(
        f"===== PIPELINE COMPLETE ({shorts_created} shorts created) ====="
    )


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Fatal error (pipeline stopped safely): {e}")
        sys.exit(0)
