import subprocess
import os

OUTPUT_PATH = "data/raw.mp4"

def download_video(video_id: str) -> str:
    """
    Downloads the full YouTube video as MP4.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"

    os.makedirs("data", exist_ok=True)

    cmd = [
        "yt-dlp",
        "-f",
        "mp4",
        "-o",
        OUTPUT_PATH,
        url,
    ]

    subprocess.run(cmd, check=True)
    return OUTPUT_PATH
