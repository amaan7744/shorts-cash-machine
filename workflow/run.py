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
    os.makedirs("data", exist_ok=True)

    video_ids = search_youtube.search_videos()
    if not video_ids:
        print("❌ No videos found")
        return

    for attempt in range(len(video_ids)):
        print(f"\n🔁 Attempt {attempt + 1}")

        video = select_video.select_video(video_ids)
        if not video:
            print("❌ No more suitable videos")
            return

        video_id = video["id"]
        print(f"🎯 Trying video: {video_id}")

        # 1. Transcript-based segment
        segment = extract_best_segment.extract_best_segment(video_id)
        if segment is None:
            print("⚠️ No transcript, skipping")
            continue

        start, end = segment

        # 2. Download
        try:
            raw_video = download_video.download_video(video_id)
        except Exception as e:
            print(f"⚠️ Download failed: {e}")
            continue

        # 3. Clip
        try:
            clip = extract_clip.extract_clip(raw_video, start=start, end=end)
        except Exception as e:
            print(f"⚠️ Clip failed: {e}")
            continue

        # 4. Script
        try:
            script = generate_script.generate_script(video_id)
        except Exception as e:
            print(f"⚠️ Script failed: {e}")
            continue

        # 5. Voice
        try:
            voice = generate_voice.generate_voice(script)
        except Exception as e:
            print(f"⚠️ Voice failed: {e}")
            continue

        # 6. Merge
        try:
            final_video = edit_short.merge(clip, voice)
        except Exception as e:
            print(f"⚠️ Merge failed: {e}")
            continue

        # 7. Upload
        try:
            upload_youtube.upload(
                video_path=final_video,
                title="Nobody expected this to happen",
                description=(
                    f"Original video by: {video['snippet']['channelTitle']}\n"
                    f"https://youtube.com/watch?v={video_id}"
                ),
            )
        except Exception as e:
            print(f"⚠️ Upload failed: {e}")
            continue

        print("✅ SUCCESS — SHORT CREATED & UPLOADED")
        return

    print("❌ All attempts failed. No video produced.")
