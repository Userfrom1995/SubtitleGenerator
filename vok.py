import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer
import datetime

def extract_audio_from_video(video_file, audio_file):
    command = f"ffmpeg -i {video_file} -ar 16000 -ac 1 -c:a pcm_s16le {audio_file}"
    subprocess.run(command, shell=True, check=True)

def format_time(seconds):
    td = datetime.timedelta(seconds=seconds)
    millis = int(td.total_seconds() * 1000) % 1000
    return str(td) + ',' + str(millis).zfill(3)

def transcribe_audio_vosk(audio_file, model_path, srt_file):
    # Load the Vosk model
    model = Model(model_path)
    
    # Open the audio file
    with wave.open(audio_file, "rb") as wf:
        # Check if the audio file is compatible with Vosk
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be mono PCM with 16kHz sample rate")
        
        # Initialize recognizer
        rec = KaldiRecognizer(model, wf.getframerate())
        
        # Read and process audio
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))
        
        # Get final results
        results.append(json.loads(rec.FinalResult()))
    
    # Write results to SRT file
    with open(srt_file, 'w') as f:
        for i, result in enumerate(results, 1):
            if 'result' in result and len(result['result']) > 0:
                start_time = format_time(result['result'][0]['start'])
                end_time = format_time(result['result'][-1]['end'])
                text = result.get('text', '')
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

    print(f"Subtitles saved to {srt_file}")

# Example usage
video_file = "a.mp4"
audio_file = "extracted_audio.wav"
model_path = "vosk-model-small-hi-0.22"
srt_file = "output_subtitle.srt"

# Step 1: Extract audio from video
extract_audio_from_video(video_file, audio_file)

# Step 2: Transcribe audio and generate subtitles
transcribe_audio_vosk(audio_file, model_path, srt_file)
