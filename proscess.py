from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler
from keras.layers import Dense, Dropout
from keras.models import Sequential
import pandas as pd
import numpy as np
import feather

# Load tracks, only select tracks that are longer than a minute
my_tracks = feather.read_dataframe('dat/my_tracks.feather').drop_duplicates().dropna().drop(['analysis_url', 'id', 'track_href', 'type'], axis=1)
unseen_tracks = feather.read_dataframe('dat/other_tracks.feather').drop_duplicates().dropna().drop(['analysis_url', 'id', 'track_href', 'type'], axis=1)

my_tracks = my_tracks[my_tracks.duration_ms > 60000]
unseen_tracks = unseen_tracks[unseen_tracks.duration_ms > 60000]


# This helps the model narrow down your music taste
# In a basic sense this just adds a 1 or 0 based on if a row in that column is between a distribution
# HELP: If someone could write a better explanation than I, it would be appreciated
t_tracks = my_tracks.drop(['time_signature', 'key', 'loudness', 'mode'], axis=1)
q = t_tracks.quantile([0.5, 1])
for i in q:
    mi, ma = q[i]
    col_name = '_' + i
    my_tracks[col_name] = ((my_tracks[i] > mi) & (my_tracks[i] < ma)).astype(int)
    unseen_tracks[col_name] = ((unseen_tracks[i] > mi) & unseen_tracks[i] < ma).astype(int)


# Fit the max_abs_scaler on all data, just in case
all_tracks = pd.concat([my_tracks, unseen_tracks], ignore_index=True).drop(['uri'], axis = 1)
max_abs_scaler = MaxAbsScaler().fit(all_tracks)

# Drop uri (Identification for the track). Not needed since we know this is data we want to train with.
my_tracks = my_tracks.drop(['uri'], axis = 1)
my_tracks = max_abs_scaler.transform(my_tracks)
rating = np.ones([len(my_tracks), 1])

# Scale all columns in unseen_tracks, except for the uri, which is a string
columns = unseen_tracks.columns.drop('uri')
unseen_tracks[columns] = max_abs_scaler.transform(unseen_tracks[columns])


x_train, x_test, y_train, y_test = train_test_split(my_tracks, rating, train_size=0.9)

# Train the model. This is the setup that worked best for me, feel free to tweak.
model = Sequential()
model.add(Dense(22, input_dim=22, activation='tanh'))
model.add(Dropout(0.5))
model.add(Dense(8))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])

model.fit(x_train, y_train, batch_size=8, epochs=8)
score = model.evaluate(x_test, y_test, batch_size=8)
print(score)

# Keep the uris seperate, values will be kept in order with predictions
unseen_tracks_uri = unseen_tracks['uri'].values
us_tracks = unseen_tracks[columns].values

#predict unseen_tracks with defined model
predictions = model.predict_proba(us_tracks)

# The threshold will likely need to be tweaked
threshold = 0.987

for i, x in enumerate(predictions):
    if x > threshold:
        print(unseen_tracks_uri[i])
