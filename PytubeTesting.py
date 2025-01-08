


import yt_dlp
import os

video = "https://music.youtube.com/search?q=Fein"


final_filename = None

def yt_dlp_monitor(self, d):
    final_filename  = d.get('info_dict').get('_filename')


with yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': '%(title)s.mp3', 'playlist_items' : '1'}) as ydl:
    info_dict = ydl.extract_info(video, download=True)
    video_url = info_dict.get("url", None)
    video_id = info_dict.get("id", None)
    video_title = info_dict.get('title', None)
    file_path = info_dict.get('_filename', None)
    print(file_path)
