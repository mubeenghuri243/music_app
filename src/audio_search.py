import subprocess
import os
import json
from acrcloud.recognizer import ACRCloudRecognizer
from src.config import ACR_HOST, ACR_KEY, ACR_SECRET

# ACRCloud config
config = {
    "host": ACR_HOST,
    "access_key": ACR_KEY,
    "access_secret": ACR_SECRET,
    "timeout": 10
}
recognizer = ACRCloudRecognizer(config)

def recognize_audio(audio_file_path):
    # Ensure unique temp WAV file
    temp_wav = os.path.abspath("temp_audio.wav")

    # Convert to WAV (mono, 44.1 kHz, PCM16, first 15 seconds)
    subprocess.run([
        "ffmpeg", "-y", "-i", audio_file_path,
        "-ac", "1", "-ar", "44100", "-sample_fmt", "s16",
        "-t", "15", temp_wav
    ], check=True)

    # Use ACRCloud file recognition
    result = recognizer.recognize_by_file(temp_wav, 0, 10)  # offset 0, duration 10s
    data = json.loads(result)
    print(f"Library Results: {data}")

    # Clean up WAV file
    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    if data['status']['code'] == 0:
        title = data["metadata"]["music"][0]["title"]
        artist = data["metadata"]["music"][0]["artists"][0]["name"]
        return title, artist
    else:
        return None