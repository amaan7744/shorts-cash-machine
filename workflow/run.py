import os, sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)

from pipeline import (
    search_reddit, download_video, extract_clip,
    generate_script, generate_voice, edit_short, upload_youtube
)

def main():
    posts = search_reddit.search_reddit()
    if not posts:
        print("No halal Reddit videos found")
        return

    post = posts[0]
    print("Using:", post["title"])

    raw = download_video.download_video(post["url"])
    clip = extract_clip.extract_clip(raw)
    script = generate_script.generate_script(post["title"])
    voice = generate_voice.generate_voice(script)
    final = edit_short.merge(clip, voice)

    upload_youtube.upload(
        final,
        "Nobody expected this to happen",
        f"Original Reddit post by u/{post['author']}"
    )

if __name__ == "__main__":
    main()
