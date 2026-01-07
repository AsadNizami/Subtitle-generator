import json
import math
import config

def seconds_to_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - math.floor(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def json_to_srt_word_level(
    filepath: str,
    outputpath: str,
    max_words_per_sub: int = 5,
    max_duration: float = 2.5
):
    """
    Convert JSON transcription to readable SRT using word-level timestamps.

    Args:
        filepath: input JSON path
        outputpath: output SRT path
        max_words_per_sub: max words per subtitle
        max_duration: max subtitle duration in seconds
    """

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    subtitle_index = 1
    current_words = []
    start_time = None

    with open(outputpath, "w", encoding="utf-8") as srt_file:
        for segment in data.get("segments", []):
            for w in segment.get("words", []):

                if start_time is None:
                    start_time = w["start"]

                current_words.append(w)

                duration = w["end"] - start_time

                # Flush subtitle if limits reached
                if (
                    len(current_words) >= max_words_per_sub
                    or duration >= max_duration
                ):
                    end_time = current_words[-1]["end"]
                    text = " ".join(word["word"] for word in current_words)

                    srt_file.write(f"{subtitle_index}\n")
                    srt_file.write(
                        f"{seconds_to_srt_time(start_time)} --> "
                        f"{seconds_to_srt_time(end_time)}\n"
                    )
                    srt_file.write(f"{text}\n\n")

                    subtitle_index += 1
                    current_words = []
                    start_time = None

        # Flush remaining words
        if current_words:
            end_time = current_words[-1]["end"]
            text = " ".join(word["word"] for word in current_words)

            srt_file.write(f"{subtitle_index}\n")
            srt_file.write(
                f"{seconds_to_srt_time(start_time)} --> "
                f"{seconds_to_srt_time(end_time)}\n"
            )
            srt_file.write(f"{text}\n\n")



if __name__ == "__main__":
    json_to_srt_word_level(config.INTERMEDIATE_JSON_NAME, config.SRT_NAME)
