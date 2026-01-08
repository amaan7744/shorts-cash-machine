import requests
import yaml
from .halal_filter import is_halal

HEADERS = {"User-Agent": "shorts-bot/1.0"}

def search_reddit():
    config = yaml.safe_load(open("config.yaml"))
    results = []

    for sub in config["reddit"]["subreddits"]:
        url = f"https://www.reddit.com/r/{sub}/top.json?limit=20&t=week"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()

        for child in r.json()["data"]["children"]:
            d = child["data"]

            if not d.get("is_video"):
                continue

            if d.get("ups", 0) < config["reddit"]["min_upvotes"]:
                continue

            if d.get("over_18"):
                continue

            media = d.get("media", {})
            rv = media.get("reddit_video")
            if not rv:
                continue

            post = {
                "id": d["id"],
                "title": d["title"],
                "url": rv["fallback_url"],
                "duration": rv["duration"],
                "author": d["author"],
                "over_18": d.get("over_18", False),
            }

            if not is_halal(post):
                continue

            if post["duration"] > config["reddit"]["max_duration_seconds"]:
                continue

            results.append(post)

    return results
