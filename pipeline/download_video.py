import requests, os

def download_video(url):
    os.makedirs("data", exist_ok=True)
    out = "data/raw.mp4"

    r = requests.get(url, stream=True, timeout=20)
    r.raise_for_status()

    with open(out, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)

    return out
