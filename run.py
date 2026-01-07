import config
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import json
import os
from convert2srt import convert2srt
import time

start = time.perf_counter()


device = config.DEVICE
torch_dtype = config.TORCH_DTYPE
model_id = config.MODEL_ID

if not os.path.exists(config.OUTPUT_DIR):
    os.makedirs(config.OUTPUT_DIR)

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True
).to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    dtype=torch_dtype,
    device=device,
)

audio_path = config.NAME

result = pipe(
    os.path.join(config.INPUT_DIR, audio_path),
    return_timestamps=True,
    language=config.OUTPUT_LANGUAGE,
    chunk_length_s=config.CHUNK_LENGTH_S,
)

json.dump(result, open(config.INTERMEDIATE_JSON_NAME, "w"))

convert2srt(config.INTERMEDIATE_JSON_NAME, config.SRT_NAME)

end = time.perf_counter()

print(f"\n==================================================\nExecution time: {end - start:.3f} seconds\n==================================================")