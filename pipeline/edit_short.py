from moviepy.editor import VideoFileClip, AudioFileClip
import os

def merge(video_path, audio_path):
    os.makedirs("data", exist_ok=True)
    output = "data/final.mp4"

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final = video.set_audio(audio)
    final.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        logger=None,
    )

    if not os.path.exists(output):
        raise RuntimeError("final.mp4 not created")

    return output
