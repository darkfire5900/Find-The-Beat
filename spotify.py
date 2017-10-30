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
        market = config.get('required', 'market')
        return client_id, client_secret, market

    def access_token(self, client_id, client_secret):
        token_url = 'https://accounts.spotify.com/api/token'
        auth = HTTPBasicAuth(client_id, client_secret)
        data = {'grant_type': 'client_credentials'}
        request_token = requests.post(token_url, data, auth=auth)
        return json.loads(request_token.text)['access_token']

    def __init__(s):
        s.client_id, s.client_secret, market = s.read_config()
        s.market = 'market=' + market
        s.amarket = '&' + s.market

    def request(s, token, url):
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(url, headers=headers)

    def make_url(s, kind=None, user=None, ids=None):
        SP = 'https://api.spotify.com/v1/'
        valid = [
            'playlist_tracks', 'related_artists', 'artist_albums',
            'album_tracks', 'track_analysis'
        ]
        if kind in valid:
            if kind is valid[0]:
                playlist = ids
                u = SP + 'users/' + user + '/playlists/' + playlist + '/tracks'
                return u
            if kind is valid[1]:
                ids = [i for i in ids if i is not None]
                u = [SP + 'artists/' + i + '/related-artists' for i in ids]
                return u
            if kind is valid[2]:
                m_t = s.market + '&album_type=single,album'
                ids = [i for i in ids if i is not None]
                u = [SP + 'artists/' + i + '/albums?' + m_t for i in ids]
                return u
            if kind is valid[3]:
                u = []
                id_chunks = [ids[x:x + 20] for x in range(0, len(ids), 20)]
                for id_chunk in id_chunks:
                    url = SP + 'albums?ids=' + ','.join(id_chunk) + s.amarket
                    u.append(url)
                return u
            if kind is valid[4]:
                u = []
                id_chunks = [ids[x:x + 100] for x in range(0, len(ids), 100)]
                for id_chunk in id_chunks:
                    url = SP + 'audio-features/?ids=' + ','.join(id_chunk)
                    u.append(url)
                return u

    def playlist_tracks(s, user, playlist_id):
        track_ids, artist_ids = [], []
        token = s.access_token(s.client_id, s.client_secret)
        url = s.make_url('playlist_tracks', user, playlist_id)
        while url is not None:
            pt = json.loads(s.request(token, url).text)
            for playlist in pt['items']:
                track = playlist['track']
                track_ids.append(track['id'])
                artist_ids.append(track['artists'][0]['id'])
            url = pt['next']
        return track_ids, artist_ids

    def related_artists(s, artist_ids):
        related_artist_ids = []
        token = s.access_token(s.client_id, s.client_secret)
        urls = s.make_url('related_artists', ids=artist_ids)
        for url in urls:
            related = json.loads(s.request(token, url).text)
            for artist in related['artists']:
                related_artist_ids.append(artist['id'])
        return related_artist_ids

    def artist_albums(s, artist_ids):
        album_ids = []
        token = s.access_token(s.client_id, s.client_secret)
        urls = s.make_url('artist_albums', ids=artist_ids)
        for url in urls:
            try:
                albums = json.loads(s.request(token, url).text)
                for album in albums['items']:
                    album_ids.append(album['id'])
            except KeyError:
                continue
        return album_ids

    def album_tracks(s, album_ids):
        track_ids = []
        token = s.access_token(s.client_id, s.client_secret)
        urls = s.make_url('album_tracks', ids=album_ids)
        for url in urls:
            albums = json.loads(s.request(token, url).text)
            for album in albums['albums']:
                tracks = album['tracks']
                for track in tracks['items']:
                    track_ids.append(track['id'])
        track_ids = [i for i in track_ids if i is not None]
        return track_ids

    def track_analysis(s, track_ids):
        analysis = []
        token = s.access_token(s.client_id, s.client_secret)
        urls = s.make_url('track_analysis', ids=track_ids)
        for url in urls:
            audio_features = json.loads(s.request(token, url).text)
            for af in audio_features['audio_features']:
                analysis.append(pd.Series(af))
        return analysis
