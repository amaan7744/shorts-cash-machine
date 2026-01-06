import sys
import os

# Ensure repo root is on PYTHONPATH
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
    # 1. Search viral videos
    video_ids = search_youtube.search_videos()
    if not video_ids:
        raise RuntimeError("No videos found")

    # 2. Select one unused viral video
    video = select_video.select_video(video_ids)
    if not video:
        raise RuntimeError("No suitable video selected")

    video_id = video["id"]

    # 3. Find best emotional segment (transcript-based)
    start, end = extract_best_segment.extract_best_segment(video_id)

    # 4. Download full video
    raw_video_path = download_video.download_video(video_id)

    # 5. Cut the clip
    clip_path = extract_clip.extract_clip(
        raw_video_path,
        start=start,
        end=end,
    )

    # 6. Generate narration script
    script_text = generate_script.generate_script(video_id)

    # 7. Generate voiceover
    voice_path = generate_voice.generate_voice(script_text)

    # 8. Merge clip + voice
    final_video = edit_short.merge(clip_path, voice_path)

    # 9. Upload to YouTube
    upload_youtube.upload(
        video_path=final_video,
        title="Nobody expected this to happen",
        description=(
            f"Original video by: {video['snippet']['channelTitle']}\n"
            f"Source: https://youtube.com/watch?v={video_id}"
        ),
    )

    print("✅ SHORT UPLOADED SUCCESSFULLY")


if __name__ == "__main__":
    main()
