import json

def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def convert2srt(json_path, srt_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)["chunks"]

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, item in enumerate(data, start=1):
            start, end = item["timestamp"]
            print(start, end)
            f.write(f"{i}\n")
            f.write(f"{seconds_to_srt_time(start)} --> {seconds_to_srt_time(end)}\n")
            f.write(item["text"].strip() + "\n\n")


if __name__ == "__main__":
    import config
    convert2srt(config.INTERMEDIATE_JSON_NAME, config.SRT_NAME)
