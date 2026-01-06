from pipeline import (
    01_search_youtube as search,
    02_select_video as select,
    03_download_video as download,
    04_extract_clip as extract,
    05_generate_script as scriptgen,
    06_generate_voice as voicegen,
    07_edit_short as editor,
    09_upload_youtube as uploader,
)
import yaml

config = yaml.safe_load(open("config.yaml"))
count = config["posting"]["uploads_per_run"]

videos = search.search_videos()

for _ in range(count):
    video = select.select_video(videos)
    if not video:
        break

    raw = download.download_video(video["id"])
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
