#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "faster-whisper",
#     "torch",
# ]
# ///

import time
import datetime
import os
from faster_whisper import WhisperModel

# ── Config ──────────────────────────────────────────────────────────────
INPUT_DIR = "input"
OUTPUT_DIR = "output"
INPUT_AUDIO_NAME = "output.wav"
INPUT_AUDIO_PATH = f"{INPUT_DIR}/{INPUT_AUDIO_NAME}"

INPUT_LANGUAGE = "zh"
MODEL_SIZE = "large-v3"
COMPUTE_TYPE = "float16"
DEVICE = "cuda"

SRT_NAME = f"{OUTPUT_DIR}/{INPUT_AUDIO_NAME.split('.')[0]}_{INPUT_LANGUAGE}.srt"

# ── Helpers ─────────────────────────────────────────────────────────────

def format_timestamp(seconds: float) -> str:
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def split_chinese_text(text: str, max_length: int = 20) -> str:
    if len(text) <= max_length:
        return text
    punctuation = ['，', '。', '！', '？', '；', ',', '.', '!', '?', ';']
    for p in punctuation:
        if p in text[10:-5]:
            parts = text.split(p, 1)
            return f"{parts[0]}{p}\n{parts[1].strip()}"
    mid = len(text) // 2
    return f"{text[:mid]}\n{text[mid:]}"

# ── Main ────────────────────────────────────────────────────────────────

def transcribe_to_srt(audio_path: str, output_file: str = SRT_NAME):
    if not os.path.exists(audio_path):
        print(f"Error: Could not find audio file at {audio_path}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading {MODEL_SIZE} model...")
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    print("Transcribing audio...")
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language=INPUT_LANGUAGE,
        condition_on_previous_text=False,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    print(f"Detected language: {info.language} with probability {info.language_probability:.2f}")

    with open(output_file, "w", encoding="utf-8") as f:
        counter = 1
        for segment in segments:
            text = segment.text.strip()
            if not text:
                continue
            text = split_chinese_text(text)
            f.write(f"{counter}\n")
            f.write(f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n")
            f.write(f"{text}\n\n")
            print(f"[{format_timestamp(segment.start)} -> {format_timestamp(segment.end)}] {text.replace(chr(10), ' ')}")
            counter += 1

    print(f"\nDone! SRT saved to {output_file}")

if __name__ == "__main__":
    start = time.time()
    transcribe_to_srt(INPUT_AUDIO_PATH)
    elapsed = time.time() - start
    minutes, seconds = divmod(elapsed, 60)
    print(f"Total time: {int(minutes)}m {seconds:.2f}s")
