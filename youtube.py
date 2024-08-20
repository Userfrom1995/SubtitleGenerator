import yt_dlp

def download_youtube_video(url, output_path="."):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = "https://youtu.be/8v-TWxPWIWc?si=k7RFbEQEZK35ugFd"  # Replace with your video URL
    download_youtube_video(video_url, output_path=".")
