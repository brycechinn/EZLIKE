import json
import secrets
import requests
import importlib

importlib.reload(secrets)

from secrets import spotify_user_id
from refresh import Refresh

class SaveSong:
    def __init__(self):

        self.user_id = spotify_user_id
        self.spotify_token = ''

    def get_current_song(self):

        query = 'https://api.spotify.com/v1/me/player/currently-playing'

        response = requests.get(query, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.spotify_token)})

        response_json = response.json()

        artists = [artist for artist in response_json['item']['artists']]
        artist_names = ', '.join([artist['name'] for artist in artists])

        song_info = {
            'id':  response_json['item']['id'],
            'song_name': response_json['item']['name'],
            'artists': artist_names
        }

        return response, song_info

    def add_to_library(self, song_info):

        query = 'https://api.spotify.com/v1/me/tracks?ids={}'.format(song_info['id'])

        response = requests.put(query, headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.spotify_token)})

        message = '"{}" by {} has been added to your library.'.format(song_info['song_name'], song_info['artists'])

        return response, message
    
    def refresh_token(self):

        refresher = Refresh()

        response, self.spotify_token = refresher.refresh()

        return response, self.spotify_token

