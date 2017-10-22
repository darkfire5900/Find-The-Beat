import pandas as pd
import feather


my_tracks = feather.read_dataframe('dat/my_tracks.feather')
other_tracks = feather.read_dataframe('dat/other_tracks.feather')

# IDEA: Add ability to dislike tracks, experiment with different scales
my_tracks['rating'] = 1
other_tracks['rating'] = 0


# Train model
