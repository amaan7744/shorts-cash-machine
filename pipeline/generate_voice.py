#!/usr/bin/env python3

import os
import sys
import random
import re
import tempfile
from typing import List

# XTTS env safety
os.environ.setdefault("COQUI_TOS_AGREED", "1")
os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")

import torch
from TTS.api import TTS
from pydub import AudioSegment, effects
from pydub.effects import compress_dynamic_range

VOICES_DIR = "voices"
SCRIPT_PATH = "data/script.txt"
OUTPUT_PATH = "data/voice.wav"

MODEL_NAME = os.environ.get(
    "TTS_MODEL_NAME",
    "tts_models/multilingual/multi-dataset/xtts_v2"
)


# ------------------ helpers ------------------ #

def log(msg: str):
    print(f"[XTTS] {msg}", flush=True)


def detect_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def read_script() -> str:
    if not os.path.exists(SCRIPT_PATH):
        log(f"ERROR: script not found: {SCRIPT_PATH}")
        sys.exit(1)

    text = open(SCRIPT_PATH, "r", encoding="utf-8").read().strip()
    if not text:
        log("ERROR: script is empty")
        sys.exit(1)

    return re.sub(r"\s+", " ", text)


def find_voice() -> str:
    if not os.path.isdir(VOICES_DIR):
        log(f"ERROR: voices dir missing: {VOICES_DIR}")
        sys.exit(1)

    voices = [
        os.path.join(VOICES_DIR, f)
        for f in os.listdir(VOICES_DIR)
        if f.lower().endswith((".wav", ".mp3"))
    ]

    if not voices:
        log("ERROR: no voice files found")
        sys.exit(1)

    choice = random.choice(voices)
    log(f"Using voice: {choice}")
    return choice


def split_text(text: str, max_words: int = 45) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current, count = [], [], 0

    for s in sentences:
        w = s.split()
        if count + len(w) <= max_words:
            current.append(s)
            count += len(w)
        else:
            chunks.append(" ".join(current))
            current = [s]
            count = len(w)

    if current:
        chunks.append(" ".join(current))

    return chunks or [text]


def normalize(seg: AudioSegment) -> AudioSegment:
    seg = effects.normalize(seg)
    seg = compress_dynamic_range(
        seg,
        threshold=-20,
        ratio=3,
        attack=5,
        release=50,
    )
    return seg.set_frame_rate(44100).set_channels(1)


# ------------------ main ------------------ #

def generate_voice(_: str = "") -> str:
    device = detect_device()
    script = read_script()
    voice = find_voice()

    log(f"Loading XTTS on {device}")
    tts = TTS(model_name=MODEL_NAME, progress_bar=False).to(device)

    chunks = split_text(script)
    pieces = []

    with tempfile.TemporaryDirectory() as tmp:
        for i, chunk in enumerate(chunks, 1):
            out = os.path.join(tmp, f"c{i}.wav")
            tts.tts_to_file(
                text=chunk,
                speaker_wav=voice,
                language="en",
                file_path=out,
            )
            pieces.append(AudioSegment.from_file(out))

    joined = pieces[0]
    silence = AudioSegment.silent(160)

    for p in pieces[1:]:
        joined = joined.append(silence + p, crossfade=20)

    final = normalize(joined)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    final.export(OUTPUT_PATH, format="wav")

    log(f"Voice written: {OUTPUT_PATH}")
    return OUTPUT_PATH
