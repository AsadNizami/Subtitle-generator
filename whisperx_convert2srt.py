import json
import re
from pathlib import Path
import config

# ==============================
# Config (Netflix-like styling)
# ==============================
MAX_CHARS_PER_LINE = 42
MAX_LINES = 2
MAX_CHARS_PER_SUB = MAX_CHARS_PER_LINE * MAX_LINES
MAX_DURATION = 6.0
MIN_DURATION = 1.0


# ==============================
# Utilities
# ==============================

def format_timestamp(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def is_sentence_end(word):
    return bool(re.search(r"[.!?]$", word))


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


# ==============================
# Fix Missing Word Timestamps
# ==============================

def fix_missing_timestamps(words):
    for i, word in enumerate(words):
        if "start" not in word or "end" not in word:

            # find previous valid word
            prev_word = None
            for j in range(i - 1, -1, -1):
                if "end" in words[j]:
                    prev_word = words[j]
                    break

            # find next valid word
            next_word = None
            for j in range(i + 1, len(words)):
                if "start" in words[j]:
                    next_word = words[j]
                    break

            if prev_word and next_word:
                word["start"] = prev_word["end"]
                word["end"] = next_word["start"]

            elif prev_word:
                word["start"] = prev_word["end"]
                word["end"] = prev_word["end"] + 0.2

            elif next_word:
                word["start"] = next_word["start"] - 0.2
                word["end"] = next_word["start"]

    return words


# ==============================
# Build Netflix-style subtitles
# ==============================

def build_subtitles(words):
    subtitles = []
    current_words = []
    start_time = None

    for word in words:

        if start_time is None:
            start_time = word["start"]

        current_words.append(word)

        # build current text
        text = clean_text(" ".join(w["word"] for w in current_words))
        duration = word["end"] - start_time

        should_break = False

        if len(text) >= MAX_CHARS_PER_SUB:
            should_break = True

        if duration >= MAX_DURATION:
            should_break = True

        if is_sentence_end(word["word"]):
            should_break = True

        if should_break:
            end_time = word["end"]
            subtitles.append((start_time, end_time, text))
            current_words = []
            start_time = None

    # remaining words
    if current_words:
        text = clean_text(" ".join(w["word"] for w in current_words))
        subtitles.append((start_time, current_words[-1]["end"], text))

    return subtitles


# ==============================
# Split into 2 balanced lines
# ==============================

def split_into_lines(text):
    if len(text) <= MAX_CHARS_PER_LINE:
        return text

    words = text.split()
    line1 = ""
    line2 = ""

    for word in words:
        if len(line1 + " " + word) <= MAX_CHARS_PER_LINE:
            line1 = (line1 + " " + word).strip()
        else:
            line2 = (line2 + " " + word).strip()

    return line1 + "\n" + line2


# ==============================
# Main Conversion Function
# ==============================

def convert_json_to_srt(json_path, output_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Prefer word_segments if available
    words = data.get("word_segments", [])

    if not words:
        # fallback
        words = []
        for seg in data["segments"]:
            words.extend(seg["words"])

    # Fix timestamp issues
    words = fix_missing_timestamps(words)

    # Remove words still missing timestamps
    words = [w for w in words if "start" in w and "end" in w]

    subtitles = build_subtitles(words)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(subtitles, 1):
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(split_into_lines(text) + "\n\n")

    print(f"✅ SRT file created at: {output_path}")


# ==============================
# Run
# ==============================

if __name__ == "__main__":
    input_json = config.INTERMEDIATE_JSON_NAME
    output_srt = config.SRT_NAME

    convert_json_to_srt(input_json, output_srt)