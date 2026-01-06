import json
import os
import yaml
from googleapiclient.discovery import build

USED_PATH = "data/used_videos.json"

def select_video(video_ids):
    config = yaml.safe_load(open("config.yaml"))
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

    used = json.load(open(USED_PATH))

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

        if views >= config["youtube"]["min_views"]:
            used.append(vid)
            json.dump(used, open(USED_PATH, "w"), indent=2)
            return video

    return None
