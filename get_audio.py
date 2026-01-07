import subprocess
import config

def extract_audio(video_path, audio_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        audio_path
    ], check=True)

NAME = f"kurzgesagt.mp4"
extract_audio(f"{config.INPUT_DIR}/{NAME}", f"{config.INPUT_DIR}/{NAME.split('.')[0]}.wav")
