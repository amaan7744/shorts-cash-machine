import subprocess
import os

def download_video(video_id: str) -> str:
    os.makedirs("data", exist_ok=True)

    cookies = os.getenv("YTDLP_COOKIES")
    if not cookies:
        raise RuntimeError("YTDLP_COOKIES secret is missing")

    cookies_path = "cookies.txt"
    with open(cookies_path, "w", encoding="utf-8") as f:
        f.write(cookies)

    output = "data/raw.mp4"
    url = f"https://www.youtube.com/watch?v={video_id}"

    result = subprocess.run(
        [
            "yt-dlp",
            "--cookies", cookies_path,
            "--no-playlist",
            "-f", "bv*[ext=mp4]+ba[ext=m4a]/mp4",
            "-o", output,
            url,
        ],
        capture_output=True,
        text=True,
    )

    print("yt-dlp STDOUT:\n", result.stdout)
    print("yt-dlp STDERR:\n", result.stderr)

    os.remove(cookies_path)

    if result.returncode != 0:
        raise RuntimeError("yt-dlp failed")

    if not os.path.exists(output):
        raise RuntimeError("raw.mp4 not created")

    return output
