#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path
from typing import Optional

import torch
from TTS.api import TTS
from pydub import AudioSegment, effects
from pydub.effects import compress_dynamic_range

# --------------------------------------------------
# ENV SAFETY (CRITICAL FOR CI)
# --------------------------------------------------
os.environ["COQUI_TOS_AGREED"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

# --------------------------------------------------
# CONFIG (LOCKED FOR ACTIONS)
# --------------------------------------------------
VOICES_DIR = Path("voices")
OUTPUT_DIR = Path("temp/audio")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

MAX_WORDS = 18            # HARD LIMIT (do NOT increase)
HOOK_SPEED = 1.08
TARGET_SR = 44100

# --------------------------------------------------
# LOGGING
# --------------------------------------------------
def log(msg: str):
    print(f"[TTS] {msg}", flush=True)

# --------------------------------------------------
# VOICE PICK (DETERMINISTIC)
# --------------------------------------------------
def pick_voice() -> Optional[Path]:
    if not VOICES_DIR.exists():
        log("voices/ directory missing")
        return None

    voices = sorted(
        p for p in VOICES_DIR.iterdir()
        if p.suffix.lower() in (".wav", ".mp3")
    )

    if not voices:
        log("No voice files found")
        return None

    log(f"Using cloned voice: {voices[0]}")
    return voices[0]

# --------------------------------------------------
# TEXT SANITIZATION
# --------------------------------------------------
def sanitize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    if len(words) > MAX_WORDS:
        text = " ".join(words[:MAX_WORDS])
    return text

# --------------------------------------------------
# AUDIO HELPERS
# --------------------------------------------------
def speed(seg: AudioSegment, factor: float) -> AudioSegment:
    return seg._spawn(
        seg.raw_data,
        overrides={"frame_rate": int(seg.frame_rate * factor)}
    ).set_frame_rate(seg.frame_rate)

def normalize(seg: AudioSegment) -> AudioSegment:
    seg = effects.normalize(seg)
    seg = compress_dynamic_range(
        seg,
        threshold=-20.0,
        ratio=3.0,
        attack=5,
        release=50,
    )
    return seg.set_channels(1).set_frame_rate(TARGET_SR)

# --------------------------------------------------
# MAIN SYNTHESIS (SAFE)
# --------------------------------------------------
def generate_hook(text: str) -> Optional[Path]:
    try:
        text = sanitize_text(text)
        if not text:
            return None

        voice = pick_voice()
        if voice is None:
            return None

        log("Loading XTTS v2 (CPU mode)")
        tts = TTS(
            model_name=MODEL_NAME,
            progress_bar=False,
            gpu=False
        )

        out_path = OUTPUT_DIR / "hook.wav"

        tts.tts_to_file(
            text=text,
            speaker_wav=str(voice),
            language="en",
            file_path=str(out_path),
        )

        seg = AudioSegment.from_file(out_path)
        seg = speed(seg, HOOK_SPEED)
        seg = normalize(seg)
        seg.export(out_path, format="wav")

        log(f"Hook voice generated: {out_path}")
        return out_path

    except Exception as e:
        log(f"TTS failed safely: {e}")
        return None
