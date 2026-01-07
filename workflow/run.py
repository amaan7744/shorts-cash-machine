import os
import sys

# -------------------------------------------------
# Ensure repo root on path
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
    print("🚀 PIPELINE STARTED")
    print("📂 CWD:", os.getcwd())

    # -------------------------------------------------
    # FORCE data dir + sentinel
    # -------------------------------------------------
    os.makedirs("data", exist_ok=True)

    with open("data/_pipeline_started.txt", "w") as f:
        f.write("pipeline reached main()\n")

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------
    video_ids = search_youtube.search_videos()
    print("🔍 Search returned:", video_ids[:5])

    if not video_ids:
        print("❌ No videos found")
        return

    # -------------------------------------------------
    # TRY VIDEOS ONE BY ONE
    # -------------------------------------------------
    for idx, _ in enumerate(video_ids):
        print(f"\n🔁 ATTEMPT {idx+1}")

        video = select_video.select_video(video_ids)
        if not video:
            print("❌ select_video returned None")
            return

        # -------------------------------------------------
        # NORMALIZE VIDEO ID (CRITICAL)
        # -------------------------------------------------
        video_id = video.get("id")

        if isinstance(video_id, dict):
            video_id = video_id.get("videoId")

        print("🎯 VIDEO ID:", video_id, type(video_id))

        if not isinstance(video_id, str):
            raise RuntimeError(f"INVALID video_id: {video_id}")

        with open("data/_before_download.txt", "w") as f:
            f.write(f"about to download {video_id}\n")

        # -------------------------------------------------
        # DOWNLOAD (STOP AFTER THIS)
        # -------------------------------------------------
        try:
            raw = download_video.download_video(video_id)
        except Exception as e:
            print("❌ DOWNLOAD FAILED:", e)
            continue

        with open("data/_after_download.txt", "w") as f:
            f.write("download finished\n")

        print("✅ DOWNLOAD SUCCESS:", raw)
        print("🛑 STOPPING PIPELINE HERE (DEBUG MODE)")
        return

    print("❌ ALL ATTEMPTS FAILED")

if __name__ == "__main__":
    main()
