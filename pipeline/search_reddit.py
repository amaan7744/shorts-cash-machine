import requests
import yaml
from .halal_filter import is_halal

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; shorts-bot/1.0)"
}

def search_reddit():
    cfg = yaml.safe_load(open("config.yaml"))
    results = []

    for sub in cfg["reddit"]["subreddits"]:
        url = f"https://old.reddit.com/r/{sub}/top/.json?raw_json=1&t=week&limit=10"

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                print(f"⚠️ Reddit blocked subreddit {sub}: {r.status_code}")
                continue

            data = r.json()
        except Exception as e:
            print(f"⚠️ Reddit fetch failed for {sub}: {e}")
            continue

        for child in data["data"]["children"]:
            d = child["data"]

            if not d.get("is_video"):
                continue
            if d.get("over_18"):
                continue
            if d.get("ups", 0) < cfg["reddit"]["min_upvotes"]:
                continue

            rv = d.get("media", {}).get("reddit_video")
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

            if post["duration"] > cfg["reddit"]["max_duration_seconds"]:
                continue
            if not is_halal(post):
                continue

            results.append(post)

    return results
