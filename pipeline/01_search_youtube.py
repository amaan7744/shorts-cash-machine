import os
import yaml
from googleapiclient.discovery import build

def search_videos():
    config = yaml.safe_load(open("config.yaml"))
    youtube = build(
        "youtube",
        "v3",
        developerKey=os.getenv("YOUTUBE_API_KEY")
    )

    video_ids = set()

    for keyword in config["youtube"]["keywords"]:
        request = youtube.search().list(
            q=keyword,
            part="id",
            type="video",
            maxResults=15,
            videoDuration="short",
            regionCode="US",              # 🔑 US BIAS
            relevanceLanguage="en",        # 🔑 English
            videoCategoryId="24"           # Entertainment
        )

        response = request.execute()

        for item in response.get("items", []):
            if "videoId" in item["id"]:
                video_ids.add(item["id"]["videoId"])

    return list(video_ids)
