import pytube
from pytube import Playlist, YouTube
import os

def download_video_with_quality(youtube, folder_name, quality_choice):
    video_streams = youtube.streams.filter(progressive=True, file_extension='mp4')
    if quality_choice == 1:  
        video_stream = video_streams.get_highest_resolution()
    else:
        print("Available video quality options:")
        for i, stream in enumerate(video_streams):
            print(f"{i + 2}. {stream.resolution} ({stream.mime_type} {stream.abr})")
        choice = int(input("Enter the number of the desired video quality (1 for best): ")) - 2
        video_stream = video_streams[choice]

    video_stream.download(output_path=folder_name)
    print(f"Successfully downloaded video: {youtube.title}")

def download_audio(youtube, folder_name):
    audio_streams = youtube.streams.filter(only_audio=True)
    print("Available audio formats:")
    audio_options = []
    for i, audio_stream in enumerate(audio_streams):
        audio_options.append(audio_stream.mime_type)
        print(f"{i + 2}. {audio_stream.mime_type} {audio_stream.abr}")
    
    choice = int(input("Enter the number of the desired audio format (1 for best): ")) - 2
    audio_stream = audio_streams[choice]
    audio_stream.download(output_path=folder_name)
    print(f"Successfully downloaded audio of video: {youtube.title}")

# Use the pytube library to fetch a playlist from YouTube
playlist_url = input("Enter the YouTube playlist URL: ")
playlist = Playlist(playlist_url)

# Create a folder to save the files with a valid folder name
folder_name = playlist.title.replace("|", "").replace(":", "").replace("?", "").replace("<", "").replace(">", "").replace("*", "")
os.makedirs(folder_name, exist_ok=True)

# Suggest downloading the playlist as audio or video
print(f"Found {len(playlist.video_urls)} videos in the playlist.")
choice = int(input("Do you want to download them all as audio (1) or video (2) files? Enter your choice: "))

quality_choice = int(input("Download the best quality available (1) or choose quality for each video manually (2)? Enter your choice: "))

# Download the videos
for video_url in playlist.video_urls:
    try:
        video = YouTube(video_url)
        if choice == 1:
            download_audio(video, folder_name)
        elif choice == 2:
            download_video_with_quality(video, folder_name, quality_choice)
        else:
            print("Invalid choice. Please enter '1' for audio or '2' for video.")
    except pytube.exceptions.AgeRestrictedError:
        print(f"The video {video_url} is age-restricted, and it has been bypassed.")
    except Exception as e:
        print(f"An error occurred while downloading the video: {str(e)}")

print("All videos have been downloaded.")

