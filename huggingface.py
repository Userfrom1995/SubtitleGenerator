from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torchaudio
import torch

def transcribe_audio_hf(audio_file, language_code='en'):
    # Load the pre-trained model and tokenizer
    model_name = "facebook/wav2vec2-large-960h" if language_code == 'en' else "facebook/wav2vec2-xls-r-2b"  # Choose a suitable model
    tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name).cuda()

    # Load and preprocess the audio file
    waveform, sample_rate = torchaudio.load(audio_file)
    inputs = tokenizer(waveform.squeeze().numpy(), return_tensors="pt", padding="longest").input_values.cuda()

    # Perform the transcription
    with torch.no_grad():
        logits = model(inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode the transcription
    transcription = tokenizer.batch_decode(predicted_ids)
    return transcription[0]

# Example usage
audio_file = "extracted_audio.wav"
language_code = "hi"  # Specify the language code if needed
transcription = transcribe_audio_hf(audio_file, language_code)
print(transcription)
