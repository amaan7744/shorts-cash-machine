from moviepy.editor import VideoFileClip

def extract_clip(video_path, start, end):
    clip = VideoFileClip(video_path)
    short = clip.subclip(start, end)

    output = "data/clip.mp4"
    short.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        threads=4,
        logger=None,
    )

    return output
