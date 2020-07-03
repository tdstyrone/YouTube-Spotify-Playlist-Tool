import os
import re
from googleapiclient.discovery import build


class YouTubeClient(object):
    def __init__(self):
        API_KEY = os.environ.get('API_KEY')
        API_SERVICE_NAME = 'youtube'
        API_VERSION = 'v3'
        yt_service = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

        pl_request = yt_service.playlists().list(
            part="contentDetails, snippet",
            channelId="UCWE8Q6StgBXgOEk-l2ze33Q"
        )
        pl_response = pl_request.execute()

        self.pl_response = pl_response
        self.yt_service = yt_service

    def get_playlist(self):
        playlist_count = 0
        url_regex = re.compile(r"([a-z0-9]+)/", re.IGNORECASE)
        options = []
        for item in self.pl_response['items']:
            pl_title = item['snippet']['title']
            playlist_count += 1
            print(f"{playlist_count}. {pl_title}")
            url_info = item['snippet']['thumbnails']['default']['url']
            url_key = url_regex.findall(url_info)
            options.append((playlist_count, url_key[2]))
        return options

    def get_songs(self, playlist_choice):
        next_page_token = None
        info_dict = {}
        songs = []
        while True:
            pl_items_request = self.yt_service.playlistItems().list(
                part="snippet",
                playlistId=self.pl_response['items'][playlist_choice].get("id"),
                maxResults=50,
                pageToken=next_page_token
            )
            pl_items_response = pl_items_request.execute()
            # Video Titles
            for item in pl_items_response['items']:
                song_title = item['snippet']['title']
                songs.append(song_title)
            next_page_token = pl_items_response.get('nextPageToken')

            if not next_page_token:
                break

        for i in range(len(songs)):
            print(f"{i + 1}. {songs[i]}")
        info_dict['Songs'] = songs
        info_dict['Playlist ID'] = self.pl_response['items'][playlist_choice].get("id")
        return info_dict

    @staticmethod
    def get_tracks_artist(songs):
        song_info = []
        for song in songs:
            song_info.append(tuple(song.split('-')))
        return song_info
