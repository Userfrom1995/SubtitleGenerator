import whisper
import ffmpeg

def extract_audio(video_file, audio_file):
    """Extracts audio from video."""
    ffmpeg.input(video_file).output(audio_file).run(overwrite_output=True)

def transcribe_audio(audio_file):
    """Transcribes audio to text using Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['segments']

def format_time(seconds):
    """Formats time from seconds to SRT format (hh:mm:ss,ms)."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def generate_srt(segments, srt_file):
    """Generates an SRT file from transcription segments."""
    with open(srt_file, "w") as file:
        for i, segment in enumerate(segments):
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text'].strip()
            file.write(f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n")

def main(video_file, output_srt):
    audio_file = "extracted_audio.wav"
    extract_audio(video_file, audio_file)
    segments = transcribe_audio(audio_file)
    generate_srt(segments, output_srt)
    print(f"Subtitle file '{output_srt}' generated successfully.")

if __name__ == "__main__":
    video_file = "/workspace/SubtitleGenerator/Humsafar (Full Video)  ｜ Varun & Alia Bhatt ｜ Akhil Sachdeva ｜ ＂Badrinath Ki Dulhania＂.mp4"  # Replace with your video file path
    output_srt = "subtitles.srt"
    main(video_file, output_srt)
