from spotify import Spotify
import configparser
import pandas as pd
import feather

s = Spotify()

config = configparser.ConfigParser()
config.read('config.ini')

USERNAME = config.get('required', 'username')
PLAYLIST_ID = config.get('required', 'playlist_uri')


track_ids, artist_ids = s.playlist_tracks(USERNAME, PLAYLIST_ID)

related_artists = set(s.related_artists(artist_ids))
related_albums = s.artist_albums(related_artists)
album_tracks = s.album_tracks(related_albums)

other_track_analysis = s.track_analysis(album_tracks)
my_track_analysis = s.track_analysis(track_ids)

other_tracks = pd.DataFrame(other_track_analysis)
my_tracks = pd.DataFrame(my_track_analysis)

feather.write_dataframe(other_tracks, 'dat/other_tracks.feather')
feather.write_dataframe(my_tracks, 'dat/my_tracks.feather')
