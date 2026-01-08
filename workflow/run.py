import os
import sys

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
    print("🚀 Shorts pipeline started")
    os.makedirs("data", exist_ok=True)

    video_ids = search_youtube.search_videos()
    if not video_ids:
        print("❌ No videos found from search")
        return

    print(f"🔍 Found {len(video_ids)} candidate videos")

    for attempt in range(len(video_ids)):
        print(f"\n🔁 Attempt {attempt + 1}")

        video = select_video.select_video(video_ids)
        if not video:
            print("❌ No selectable video remaining")
            return

        video_id = video.get("id")
        if isinstance(video_id, dict):
            video_id = video_id.get("videoId")

        if not isinstance(video_id, str):
            print("⚠️ Invalid video ID, skipping")
            continue

        print(f"🎯 Trying video: {video_id}")

        # -------------------------------------------------
        # SEGMENT (never blocks due to fallback)
        # -------------------------------------------------
        try:
            start, end = extract_best_segment.extract_best_segment(video_id)
        except Exception as e:
            print(f"⚠️ Segment detection failed: {e}")
            continue

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------
        try:
            raw = download_video.download_video(video_id)
        except Exception as e:
            print(f"⚠️ Download failed: {e}")
            continue

        # -------------------------------------------------
        # CLIP
        # -------------------------------------------------
        try:
            clip = extract_clip.extract_clip(raw, start, end)
        except Exception as e:
            print(f"⚠️ Clip extraction failed: {e}")
            continue

        # -------------------------------------------------
        # SCRIPT
        # -------------------------------------------------
        try:
            script = generate_script.generate_script()
        except Exception as e:
            print(f"⚠️ Script generation failed: {e}")
            continue

        # -------------------------------------------------
        # VOICE
        # -------------------------------------------------
        try:
            voice = generate_voice.generate_voice(script)
        except Exception as e:
            print(f"⚠️ Voice generation failed: {e}")
            continue

        # -------------------------------------------------
        # MERGE
        # -------------------------------------------------
        try:
            final = edit_short.merge(clip, voice)
        except Exception as e:
            print(f"⚠️ Merge failed: {e}")
            continue

        # -------------------------------------------------
        # UPLOAD
        # -------------------------------------------------
        try:
            upload_youtube.upload(
                video_path=final,
                title="Nobody expected this to happen",
                description=(
                    f"Original video:\n"
                    f"https://youtube.com/watch?v={video_id}"
                ),
            )
        except Exception as e:
            print(f"⚠️ Upload failed: {e}")
            continue

        print("✅ SUCCESS — Short created and uploaded")
        return

    print("❌ All attempts failed. No short created.")

if __name__ == "__main__":
    main()
