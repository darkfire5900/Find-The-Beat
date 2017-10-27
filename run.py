from spotify import Spotify
import configparser
import pandas as pd
import feather

s = Spotify()

config = configparser.ConfigParser()
config.read('config.ini')

USERNAME = config.get('required', 'username')
PLAYLIST_ID = config.get('required', 'playlist_uri')


track_ids, artist_ids = s.return_track_artist_ids(USERNAME, PLAYLIST_ID)

related_artists = set(s.return_related_artists(artist_ids))
related_albums = s.return_artists_albums(related_artists)
album_tracks = s.return_artist_album_tracks(related_albums)

other_track_analysis = s.return_track_analysis(album_tracks)
my_track_analysis = s.return_track_analysis(track_ids)

df = pd.DataFrame(other_track_analysis)
df2 = pd.DataFrame(my_track_analysis)


feather.write_dataframe(df, 'dat/other_tracks.feather')
feather.write_dataframe(df2, 'dat/my_tracks.feather')
