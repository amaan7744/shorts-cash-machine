from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_captions(video_path, script):
    video = VideoFileClip(video_path)

    words = script.split()
    clips = []

    duration_per_word = video.duration / len(words)
    t = 0

    for word in words:
        txt = TextClip(
            word.upper(),
            fontsize=80,
            color="white",
            stroke_color="black",
            stroke_width=2,
            font="Arial-Bold"
        ).set_position("center").set_duration(duration_per_word).set_start(t)

        clips.append(txt)
        t += duration_per_word

    final = CompositeVideoClip([video] + clips)
    output = "data/final_captioned.mp4"
    final.write_videofile(output, codec="libx264")

    return output
