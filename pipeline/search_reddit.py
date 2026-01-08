import requests
import yaml
import random
from .halal_filter import is_halal

INSTANCES = [
    "https://libredd.it",
    "https://libreddit.de",
    "https://lr.riverside.rocks",
    "https://redlib.catsarch.com",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_json(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}")
    return r.json()

def search_reddit():
    cfg = yaml.safe_load(open("config.yaml"))
    results = []

    for sub in cfg["reddit"]["subreddits"]:
        random.shuffle(INSTANCES)

        data = None
        for base in INSTANCES:
            url = f"{base}/r/{sub}/top.json?limit=10&t=week"
            try:
                data = fetch_json(url)
                break
            except Exception as e:
                print(f"⚠️ {base} failed for {sub}: {e}")

        if not data:
            print(f"❌ All instances failed for {sub}")
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
