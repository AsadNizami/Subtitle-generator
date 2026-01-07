# srtgen

Automated SRT subtitle generation from video using WhisperX and Transformers.

This project provides tools to extract audio from video files, transcribe them using OpenAI's Whisper models, align the text at the word level, and generate SRT subtitle files.

## Features

- **Audio Extraction**: Uses FFmpeg to extract mono audio at 16kHz.
- **Batched Transcription**: Supports efficient transcription using WhisperX.
- **Word-Level Alignment**: Provides precise timestamps for individual words.
- **SRT Generation**: Converts transcription results into standard subtitle format.

## Prerequisites

- **FFmpeg**: Required for audio extraction.
- **Nvidia GPU**: Recommended for faster transcription (CUDA support).
- **uv**: Python package and project manager.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd srtgen

# Install dependencies
uv sync
```

## Usage

### 1. Configure the Project

Edit `config.py` to set your input file paths, model ID, and language preferences.

### 2. Extract Audio

If you have a video file, extract the audio first:

```bash
uv run get_audio.py
```

### 3. Generate Subtitles

You can use the WhisperX pipeline for better alignment:

```bash
uv run whisperx_convert2json.py
uv run whisperx_convert2srt.py
```

Alternatively, use the Transformers-based pipeline in `run.py`:

```bash
uv run run.py
```

## Configuration

The `config.py` file contains several important settings:

- `DEVICE`: Computing device (`cuda:0` or `cpu`).
- `MODEL_ID`: The Whisper model to use (e.g., `openai/whisper-large-v3`).
- `INPUT_DIR`: Directory for input video/audio files.
- `OUTPUT_DIR`: Directory where JSON and SRT files will be saved.
- `OUTPUT_LANGUAGE`: Language of the transcription (e.g., `en`).
