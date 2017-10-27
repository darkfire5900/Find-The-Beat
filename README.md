# Find-The-Beat
Building a recommendation engine using data available via the Spotify API.

USAGE:
Navigate to https://developer.spotify.com/my-applications/#!/applications; obtain client id and secret.
Paste client id and secret in config.ini

Make a public playlist with songs you would like more of, the more the better
Make sure you use the playlist owners username.
Right click the playlist, share, copy URI, paste URI, and username in config.ini

Run run.py to collect data from your songs, and collect a ton of songs from other artists.
For a playlist with 700 songs, this took about half an hour, will also depend on your internet connection, be patient.

Run train.py, it will spit out a list of URIs of similar songs in the console, copy those and and CTRL + V into an empty Spotify playlist

Enjoy, friends.
