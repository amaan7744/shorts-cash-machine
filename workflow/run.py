from pipeline import (
    _01_search_youtube as search,
    _02_select_video as select,
    _04_extract_clip as extract,
    _05_generate_script as scriptgen,
    _06_generate_voice as voicegen,
    _07_edit_short as editor,
    _09_upload_youtube as uploader,
)

videos = search.search_videos()
video = select.select_video(videos)

raw = f"https://www.youtube.com/watch?v={video['id']}"
clip = extract.extract_clip(raw, video["id"])

script = scriptgen.generate_script()
voice = voicegen.generate_voice(script)

final = editor.merge(clip, voice)

uploader.upload(
    final,
    title="Nobody expected this to happen",
    description=(
        f"Original video by: {video['snippet']['channelTitle']}\n"
        f"Source: https://youtube.com/watch?v={video['id']}"
    )
)
