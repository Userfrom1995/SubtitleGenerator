import subprocess

def convert_mp4_to_mp3(input_file, output_file):
    # Construct the ffmpeg command to convert MP4 to MP3
    command = [
        'ffmpeg',
        '-i', input_file,  # Input file
        '-vn',             # No video
        '-acodec', 'mp3',  # Audio codec
        '-q:a', '2',       # Quality level (2 is good quality)
        output_file        # Output file
    ]
    
    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful! {output_file} created.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Example usage
input_file = "a.mp4"
output_file = "output_audio.mp3"
convert_mp4_to_mp3(input_file, output_file)
