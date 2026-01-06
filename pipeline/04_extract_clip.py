from moviepy.editor import VideoFileClip
from pipeline.03b_extract_best_segment import extract_best_segment

def extract_clip(path, video_id):
    clip = VideoFileClip(path)

    start, end = extract_best_segment(video_id)
    short = clip.subclip(start, end)

    output = "data/clip.mp4"
    short.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=30
    )

    return output
