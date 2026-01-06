import json
import os
import yaml
from googleapiclient.discovery import build

USED_PATH = "data/used_videos.json"
BLACKLIST_PATH = "data/creators_blacklist.txt"

def load_blacklist():
    if not os.path.exists(BLACKLIST_PATH):
        return set()
    return set(
        line.strip().lower()
        for line in open(BLACKLIST_PATH, "r", encoding="utf-8")
        if line.strip()
    )

def select_video(video_ids):
    config = yaml.safe_load(open("config.yaml"))
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

    used = json.load(open(USED_PATH))
    blacklist = load_blacklist()

    for vid in video_ids:
        if vid in used:
            continue

        res = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=vid
        ).execute()

        if not res["items"]:
            continue

        video = res["items"][0]
        views = int(video["statistics"].get("viewCount", 0))
        channel = video["snippet"]["channelTitle"].lower()

        if channel in blacklist:
            continue

        if views >= config["youtube"]["min_views"]:
            used.append(vid)
            json.dump(used, open(USED_PATH, "w"), indent=2)
            return video

    return None
