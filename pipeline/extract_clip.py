from moviepy.editor import VideoFileClip
import os

def extract_clip(video_path, start, end):
    os.makedirs("data", exist_ok=True)
    output = "data/clip.mp4"

    clip = VideoFileClip(video_path).subclip(start, end)
    clip.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        logger=None,
    )

    if not os.path.exists(output):
        raise RuntimeError("clip.mp4 not created")

    return output
