# Whisper Speech-to-Text (STT) Integration

import whisper
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import numpy as np
import google.generativeai as genai
import time

# Configure Gemini API (you'll need an API key)
genai.configure(api_key="AIzaSyBLcu1rXpEYMRvGPdKvzjiGigFOnk-q4tA")  # Replace with your actual API key

# Load Whisper model locally
def load_whisper_model(model_size="base"):
    """
    Load Whisper model from Hugging Face transformers.
    Available sizes: tiny, base, small, medium, large
    Smaller models are faster but less accurate.
    """
    print(f"Loading Whisper {model_size} model...")
    processor = WhisperProcessor.from_pretrained(f"openai/whisper-{model_size}")
    model = WhisperForConditionalGeneration.from_pretrained(f"openai/whisper-{model_size}")
    
    # Move to GPU if available
    if torch.cuda.is_available():
        model = model.to("cuda")
        print("Using GPU for inference")
    else:
        print("Using CPU for inference")
    
    return model, processor

# Transcribe audio using local Whisper model
def transcribe_audio_local(audio_path, model_size="base"):
    # Load model
    model, processor = load_whisper_model(model_size)
    
    # Load and preprocess audio
    print("Converting audio...")
    audio = AudioSegment.from_file(audio_path)
    # Convert to mono and resample to 16kHz
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    
    # Convert audio to numpy array
    audio_array = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    
    # Process audio
    print("Transcribing...")
    start_time = time.time()
    
    input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
    if torch.cuda.is_available():
        input_features = input_features.to("cuda")
        
    # Generate tokens and then text
    predicted_ids = model.generate(
        input_features,
        language="en",  # Force English transcription/translation
        task="transcribe"  # Explicitly set task to transcribe (not translate)
    )
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    
    elapsed_time = time.time() - start_time
    print(f"Transcription completed in {elapsed_time:.2f} seconds")
    
    return transcription

# Process interview response using Gemini
def process_response_with_gemini(transcribed_text):
    prompt = f"Analyze this interview response: '{transcribed_text}'. Provide a structured JSON output with key insights, formatted as valid JSON **only valid JSON**, without markdown or code formatting."
    
    # Use the correct google.generativeai syntax
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text

# Example usage
#try:
    # Choose model size based on your needs:
    # - "tiny" or "base" for quick results (less accurate)
    # - "small" for balanced speed/accuracy
    # - "medium" or "large" for best accuracy (slower)
#    model_size = "base"  # Change as needed
    
#    transcribed_text = transcribe_audio_local(
#        "interview_answer.mp3", 
#        model_size=model_size
#    )
#    print("\nTranscribed Text:", transcribed_text)
    
#    ai_analysis = process_response_with_gemini(transcribed_text)
#    print("\nAI Analysis:", ai_analysis)
#except Exception as e:
#    print(f"Error: {str(e)}")