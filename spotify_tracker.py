import requests
import json

class SpotifyTracker:


    def __init__(self, access_token) -> None:
        self.access_token = access_token


    def get_current_song(self):
        print("Grabbing song currently playing")
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token),
            'Accept': "application/json",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers).json()

        artist = response.get("item").get("artists")[0].get("name")
        album = response.get("item").get("album").get("name")
        song = response.get('item').get('name')

        return(self.song_data_struct(song, artist, album))


    def song_data_struct(self, song, artist, album):
        return {
            "song": song,
            "artist": artist,
            "album": album
        }
