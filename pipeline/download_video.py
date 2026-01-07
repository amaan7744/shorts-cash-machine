import subprocess
import os

def download_video(video_id: str) -> str:
    os.makedirs("data", exist_ok=True)
    output = "data/raw.mp4"

    url = f"https://www.youtube.com/watch?v={video_id}"

    subprocess.run(
        [
            "yt-dlp",
            "-f",
            "mp4",
            "-o",
            output,
            url,
        ],
        check=True,
    )

    if not os.path.exists(output):
        raise RuntimeError("raw.mp4 not created")

    return output
