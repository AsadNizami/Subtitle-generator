import whisperx
import gc
import json
from whisperx.diarize import DiarizationPipeline
import config


device = "cuda"
audio_file = config.INPUT_AUDIO_PATH
batch_size = 8 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("large-v3", device, compute_type=compute_type)

# save model to local path (optional)
# model_dir = "/path/"
# model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size, language=config.OUTPUT_LANGUAGE)
print(result["segments"]) # before alignment

# delete model if low on GPU resources
import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

# print(result["segments"]) 
json.dump(result, open(config.INTERMEDIATE_JSON_NAME, "w"))