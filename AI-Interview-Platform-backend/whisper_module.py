import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
import asyncio
import queue
import threading

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

async def stream_transcribe_audio(websocket, duration=30, fs=16000):
    audio_queue = queue.Queue()
    transcription = []

    def audio_callback(indata, frames, time, status):
        audio_queue.put(indata.copy())

    def process_audio(model, processor):
        while not audio_queue.empty():
            audio_data = audio_queue.get()
            audio_array = audio_data.flatten().astype(np.float32) / 32768.0
            input_features = processor(audio_array, sampling_rate=fs, return_tensors="pt").input_features
            if torch.cuda.is_available():
                input_features = input_features.to("cuda")
            predicted_ids = model.generate(input_features)
            text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            if text.strip():
                transcription.append(text)

    model, processor = load_whisper_model("tiny")  # Use tiny model for speed
    stream = sd.InputStream(samplerate=fs, channels=1, callback=audio_callback)
    stream.start()

    try:
        start_time = asyncio.get_event_loop().time()
        while (asyncio.get_event_loop().time() - start_time) < duration:
            if not audio_queue.empty():
                threading.Thread(target=process_audio, args=(model, processor), daemon=True).start()
            await asyncio.sleep(0.1)
        stream.stop()
        stream.close()
        return " ".join(transcription) if transcription else ""
    except Exception as e:
        print(f"Streaming error: {e}")
        return ""