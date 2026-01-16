import whisper
from logger import logger
from config import SUB_DIR

model = whisper.load_model("tiny")

def transcribe_clip(clip_path):
    try:
        result = model.transcribe(str(clip_path), fp16=False)
        srt = SUB_DIR / (clip_path.stem + ".srt")

        with open(srt, "w", encoding="utf-8") as f:
            for i, seg in enumerate(result["segments"], 1):
                f.write(f"{i}\n")
                f.write(
                    f"{format_ts(seg['start'])} --> {format_ts(seg['end'])}\n"
                )
                f.write(seg["text"].strip() + "\n\n")

        return srt
    except Exception as e:
        logger.error(f"Subtitle failed: {e}")
        return None

def format_ts(seconds):
    ms = int((seconds % 1) * 1000)
    s = int(seconds)
    h = s // 3600
    m = (s % 3600) // 60
    s = s % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
