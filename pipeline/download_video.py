import subprocess
import os

def download_video(video_id: str) -> str:
    os.makedirs("data", exist_ok=True)

    output = "data/raw.mp4"
    url = f"https://www.youtube.com/watch?v={video_id}"

    print("📥 yt-dlp URL:", url)

    result = subprocess.run(
        [
            "yt-dlp",
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o",
            output,
            url,
        ],
        capture_output=True,
        text=True,
    )

    print("📤 yt-dlp STDOUT:\n", result.stdout)
    print("📛 yt-dlp STDERR:\n", result.stderr)

    if result.returncode != 0:
        raise RuntimeError("yt-dlp failed")

    if not os.path.exists(output):
        raise RuntimeError("raw.mp4 NOT CREATED")

    return output
