from requests.auth import HTTPBasicAuth
import ujson as json
import pandas as pd
import configparser
import requests


class Spotify():

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        client_id = config.get('required', 'client_id')
        client_secret = config.get('required', 'client_secret')
        return client_id, client_secret

    def __init__(self):
        self.client_id, self.client_secret = self.read_config()
        self.API = 'https://api.spotify.com/v1/'

    def return_token(self, client_id, client_secret):
        token_url = 'https://accounts.spotify.com/api/token'
        auth = HTTPBasicAuth(client_id, client_secret)
        data = {'grant_type': 'client_credentials'}
        request_token = requests.post(token_url, data, auth=auth)
        return json.loads(request_token.text)['access_token']

    def return_request(self, token, url):
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(url, headers=headers)

    def return_track_artist_ids(self, user, playlist):
        track_ids, artist_ids = [], []
        token = self.return_token(self.client_id, self.client_secret)
        url = self.API + 'users/' + user + '/playlists/' + playlist + '/tracks'
        while url is not None:
            track_data = json.loads(self.return_request(token, url).text)
            for item in track_data['items']:
                track = item['track']
                track_ids.append(track['id'])
                artist_ids.append(track['artists'][0]['id'])
            url = track_data['next']
        return track_ids, artist_ids

    def return_related_artists(self, ids):
        related_artists = []
        token = self.return_token(self.client_id, self.client_secret)
        urls = [self.API + 'artists/' + i + '/related-artists' for i in ids]
        for url in urls:
            related = json.loads(self.return_request(token, url).text)
            for artists in related['artists']:
                related_artists.append(artists['id'])
        return related_artists

    def return_artists_albums(self, ids):
        album_ids = []
        token = self.return_token(self.client_id, self.client_secret)
        urls = [self.API + 'artists/' + i + '/albums?market=CA' for i in ids]
        for url in urls:
            albums = json.loads(self.return_request(token, url).text)
            for i in albums['items']:
                album_ids.append(i['id'])
        return album_ids

    def return_artist_album_tracks(self, ids):
        artist_tracks = []
        token = self.return_token(self.client_id, self.client_secret)
        id_chunks = [ids[x:x + 20] for x in range(0, len(ids), 20)]
        for id_chunk in id_chunks:
            url = self.API + 'albums?ids=' + ','.join(id_chunk) + '&market=CA'
            albums = json.loads(self.return_request(token, url).text)
            for album in albums['albums']:
                tracks = album['tracks']
                for track in tracks['items']:
                    track_id = track['id']
                    if type(track_id) is not None:
                        artist_tracks.append(track['id'])
        return artist_tracks

    def return_track_analysis(self, ids):
        track_analysis = []
        token = self.return_token(self.client_id, self.client_secret)
        id_chunks = [ids[x:x + 100] for x in range(0, len(ids), 100)]
        for id_chunk in id_chunks:
            url = self.API + 'audio-features/?ids=' + ','.join(id_chunk)
            audio_features = json.loads(self.return_request(token, url).text)
            for item in audio_features['audio_features']:
                track_analysis.append(pd.Series(item))
        return track_analysis
