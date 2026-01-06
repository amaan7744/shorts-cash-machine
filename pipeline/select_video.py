import json
import os
import yaml
from googleapiclient.discovery import build

USED_PATH = "data/used_videos.json"


def load_used_videos():
    """
    Safely load used video IDs.
    Handles:
    - missing file
    - empty file
    - invalid JSON
    """
    if not os.path.exists(USED_PATH):
        return []

    try:
        with open(USED_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []


def save_used_videos(used):
    os.makedirs(os.path.dirname(USED_PATH), exist_ok=True)
    with open(USED_PATH, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2)


def select_video(video_ids):
    config = yaml.safe_load(open("config.yaml"))
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

    used = load_used_videos()

    for vid in video_ids:
        if vid in used:
            continue

        res = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=vid
        ).execute()

        if not res.get("items"):
            continue

        video = res["items"][0]
        views = int(video["statistics"].get("viewCount", 0))

        if views >= config["youtube"]["min_views"]:
            used.append(vid)
            save_used_videos(used)
            return video

    return None
