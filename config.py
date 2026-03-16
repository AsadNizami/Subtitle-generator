import torch


DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

INPUT_DIR = "input"

OUTPUT_DIR = "output"
INPUT_AUDIO_NAME = "output.wav"

INPUT_AUDIO_PATH = f"{INPUT_DIR}/{INPUT_AUDIO_NAME}"

MODEL_ID = "openai/whisper-large-v3"
CHUNK_LENGTH_S = None

INPUT_LANGUAGE = "zh"
OUTPUT_LANGUAGE = "zh"
TASK = "transcribe" # "transcribe" or "translate"

INTERMEDIATE_JSON_NAME = f"{OUTPUT_DIR}/{INPUT_AUDIO_NAME.split('.')[0]}_{OUTPUT_LANGUAGE}.json"
SRT_NAME = f"{OUTPUT_DIR}/{INPUT_AUDIO_NAME.split('.')[0]}_{OUTPUT_LANGUAGE}.srt"

# export LD_LIBRARY_PATH=$PWD/.venv/lib/python3.12/site-packages/nvidia/cudnn/lib:$LD_LIBRARY_PATH
# whisperx version 3.3.1
# export LD_LIBRARY_PATH=$(python -c "import nvidia.cudnn; print(nvidia.cudnn.__path__[0] + '/lib')"):$LD_LIBRARY_PATH