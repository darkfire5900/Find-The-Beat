from modules import spotify_authorization, se_to_json_to_playlist_ids, search_and_convert_to_json, playlist_ids_to_tracks
import time
import simplejson as json
import sqlite3

token = spotify_authorization("", "")


se_terms = ["modern 80s", "modern funk", "modern disco", "modern groovy", "indie funk", "unique", "soul"]
se = se_to_json_to_playlist_ids(se_terms, "playlist", 20)
print(len(se))

se_ = []
for i in se:
    if i not in se_:
        se_.append(i)
print(len(se_))

conn = sqlite3.connect('song_ids.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE playlist_data(playlist_data text)''')

pitt = playlist_ids_to_tracks(se_)
print(len(pitt))
for i in pitt:
    time.sleep(0.005)
    try:
        j = json.loads(i.text)
        items = j["items"]
        for i in j["items"]:
            track = i["track"]
            c.execute("INSERT INTO playlist_data VALUES" + "('" + track["id"] + "')")
    except Exception:
        pass

select = c.execute('SELECT * FROM playlist_data')
for i, row in enumerate(select):
    print(i, row[0])

conn.close()