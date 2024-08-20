import whisper
import ffmpeg
from googletrans import Translator

def extract_audio(video_file, audio_file):
    """Extracts audio from video."""
    ffmpeg.input(video_file).output(audio_file).run(overwrite_output=True)

def transcribe_audio(audio_file, language):
    """Transcribes audio to text using Whisper in the specified language."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, language=language)  # Use the specified language
    return result['segments']

def format_time(seconds):
    """Formats time from seconds to SRT format (hh:mm:ss,ms)."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def translate_text(text, target_language):
    """Translates text to the target language using Google Translate."""
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def generate_srt(segments, srt_file, target_language=None):
    """Generates an SRT file from transcription segments.
    
    If target_language is None, the subtitles will be in the original language of the video.
    """
    with open(srt_file, "w") as file:
        for i, segment in enumerate(segments):
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text'].strip()

            if target_language:
                text = translate_text(text, target_language)

            file.write(f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n")

def main(video_file, output_srt, language, target_language=None):
    audio_file = "extracted_audio.wav"
    extract_audio(video_file, audio_file)
    segments = transcribe_audio(audio_file, language)
    
    if target_language is None:
        print(f"Generating subtitles in the original language: {language}")
    else:
        print(f"Translating subtitles to: {target_language}")

    generate_srt(segments, output_srt, target_language)
    print(f"Subtitle file '{output_srt}' generated successfully.")

if __name__ == "__main__":
    video_file = "Humsafar (Full Video)  ｜ Varun & Alia Bhatt ｜ Akhil Sachdeva ｜ ＂Badrinath Ki Dulhania＂.mp4"  # Replace with your video file path
    output_srt = "subtitles.srt"
    language = "hi"  # Specify the language code of the video (e.g., "hi" for Hindi)
    target_language = None  # Set to None for subtitles in the original language, or specify a different language code
    main(video_file, output_srt, language, target_language)
