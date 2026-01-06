import sys
import os

# -------------------------------------------------
# Ensure repo root is on PYTHONPATH
# -------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from pipeline import (
    search_youtube,
    select_video,
    extract_best_segment,
    download_video,
    extract_clip,
    generate_script,
    generate_voice,
    edit_short,
    upload_youtube,
)


def main():
    print("🚀 Starting Shorts pipeline")

    # -------------------------------------------------
    # 1. Search viral videos
    # -------------------------------------------------
    video_ids = search_youtube.search_videos()
    if not video_ids:
        print("❌ No videos found from search")
        return

    # -------------------------------------------------
    # 2. Select a candidate video
    # -------------------------------------------------
    video = select_video.select_video(video_ids)
    if not video:
        print("❌ No suitable video passed filters")
        return

    video_id = video["id"]
    print(f"🎯 Selected video: {video_id}")

    # -------------------------------------------------
    # 3. Transcript-based segment detection
    # -------------------------------------------------
    segment = extract_best_segment.extract_best_segment(video_id)
    if segment is None:
        print(f"⚠️ No transcript available for {video_id}. Skipping.")
        return

    start, end = segment
    print(f"✂️ Selected segment: {start:.2f}s → {end:.2f}s")

    # -------------------------------------------------
    # 4. Download full video
    # -------------------------------------------------
    try:
        raw_video_path = download_video.download_video(video_id)
    except Exception as e:
        print(f"❌ Video download failed: {e}")
        return

    # -------------------------------------------------
    # 5. Extract clip
    # -------------------------------------------------
    try:
        clip_path = extract_clip.extract_clip(
            raw_video_path,
            start=start,
            end=end,
        )
    except Exception as e:
        print(f"❌ Clip extraction failed: {e}")
        return

    # -------------------------------------------------
    # 6. Generate narration script
    # -------------------------------------------------
    try:
        script_text = generate_script.generate_script(video_id)
    except Exception as e:
        print(f"❌ Script generation failed: {e}")
        return

    # -------------------------------------------------
    # 7. Generate voiceover
    # -------------------------------------------------
    try:
        voice_path = generate_voice.generate_voice(script_text)
    except Exception as e:
        print(f"❌ Voice generation failed: {e}")
        return

    # -------------------------------------------------
    # 8. Merge clip + voice
    # -------------------------------------------------
    try:
        final_video = edit_short.merge(clip_path, voice_path)
    except Exception as e:
        print(f"❌ Video merge failed: {e}")
        return

    # -------------------------------------------------
    # 9. Upload to YouTube Shorts
    # -------------------------------------------------
    try:
        upload_youtube.upload(
            video_path=final_video,
            title="Nobody expected this to happen",
            description=(
                f"Original video by: {video['snippet']['channelTitle']}\n"
                f"Source: https://youtube.com/watch?v={video_id}"
            ),
        )
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return

    print("✅ SHORT UPLOADED SUCCESSFULLY")


if __name__ == "__main__":
    main()
