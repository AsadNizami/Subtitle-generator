#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "faster-whisper",
#     "torch",
# ]
# ///

import datetime
import os
import config
from faster_whisper import WhisperModel

# 1. Load Model (large-v3 in float16 uses ~3.1GB VRAM, well under your 8GB limit)
model_size = "large-v3"
print(f"Loading {model_size} model...")
model = WhisperModel(model_size, device="cuda", compute_type="float16")

def format_timestamp(seconds: float) -> str:
    """Converts seconds (float) to SRT timestamp format: HH:MM:SS,mmm"""
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def split_chinese_text(text: str, max_length: int = 20) -> str:
    """Splits long lines gracefully without cutting words in half."""
    if len(text) <= max_length:
        return text
    
    punctuation = ['，', '。', '！', '？', '；', ',', '.', '!', '?', ';']
    for p in punctuation:
        if p in text[10:-5]: 
            parts = text.split(p, 1)
            return f"{parts[0]}{p}\n{parts[1].strip()}"
            
    mid = len(text) // 2
    return f"{text[:mid]}\n{text[mid:]}"

def transcribe_to_srt(audio_path: str, output_file: str = "final_subs.srt"):
    """Transcribes audio and writes directly to an SRT file."""
    if not os.path.exists(audio_path):
        print(f"Error: Could not find audio file at {audio_path}")
        return

    print("Transcribing audio...")
    
    segments, info = model.transcribe(
        audio_path, 
        beam_size=5, 
        language="zh",
        condition_on_previous_text=False,
        vad_filter=True, 
        vad_parameters=dict(min_silence_duration_ms=500)
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

# 2. Execute
if __name__ == "__main__":
    audio_path = config.INPUT_AUDIO_PATH
    transcribe_to_srt(audio_path, output_file="final_subs.srt")