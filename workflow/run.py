import os
import sys

# Ensure repo root is on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from pipeline import (
    search_reddit,
    download_video,
    extract_clip,
    generate_script,
    generate_voice,
    edit_short,
    upload_youtube,
)

def main():
    posts = search_reddit.search_reddit()

    if not posts:
        print("❌ No halal Reddit videos found")
        return

    post = posts[0]
    print("✅ Selected Reddit post:", post["title"])

    raw = download_video.download_video(post["url"])
    print("📥 raw.mp4 created")

    clip = extract_clip.extract_clip(raw)
    print("✂️ clip.mp4 created")

    script = generate_script.generate_script(post["title"])
    print("📝 script.txt created")

    voice = generate_voice.generate_voice(script)
    print("🎙️ voice.wav created")

    final = edit_short.merge(clip, voice)
    print("🎬 final.mp4 created")

    upload_youtube.upload(
        final,
        title="Nobody expected this to happen",
        description=f"Original Reddit post by u/{post['author']}"
    )

    print("🚀 Upload completed")

if __name__ == "__main__":
    main()
