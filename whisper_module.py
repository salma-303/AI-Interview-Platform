import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import numpy as np
import time

def load_whisper_model(model_size="base"):
    processor = WhisperProcessor.from_pretrained(f"openai/whisper-{model_size}")
    model = WhisperForConditionalGeneration.from_pretrained(f"openai/whisper-{model_size}")
    if torch.cuda.is_available():
        model = model.to("cuda")
    return model, processor

def transcribe_audio_local(audio_path, model_size="base"):
    model, processor = load_whisper_model(model_size)
    audio = AudioSegment.from_file(audio_path).set_channels(1).set_frame_rate(16000)
    audio_array = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
    if torch.cuda.is_available():
        input_features = input_features.to("cuda")
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription