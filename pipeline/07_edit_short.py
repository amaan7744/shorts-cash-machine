from moviepy.editor import VideoFileClip, AudioFileClip

def merge(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final = video.set_audio(audio)
    output = "data/final.mp4"

    final.write_videofile(output, codec="libx264", audio_codec="aac")
    return output
