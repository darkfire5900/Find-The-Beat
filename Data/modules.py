from tomorrow import threads
from requests.auth import HTTPBasicAuth
import requests
import simplejson as json

def spotify_authorization(client_id, client_secret):
    auth = HTTPBasicAuth(client_id, client_secret)
    r = requests.post("https://accounts.spotify.com/api/token", auth=auth, data = {'grant_type':'client_credentials'})
    j = json.loads(r.text)
    return(j["access_token"])

token = spotify_authorization("", "")


def search_handler(search_terms, return_type, iterations):
    for search_term in search_terms:
        searches = []
        iterations = iterations * 10 + 1
        for i in range(0, iterations, 50):
            i = str(i)
            payload = "https://api.spotify.com/v1/search?q=" + search_term + "&type=" + return_type + "&limit=50" + "&offset=" + i
            r = payload_injection(payload)
            searches.append(r)
        return searches


@threads(8)
def payload_injection(payload):
    r = requests.get(payload, headers={"Authorization": "Bearer " + token})
    return r


@threads(8)
def payload_injection_slow(payload):
    r = requests.get(payload, headers={"Authorization": "Bearer " + token})
    return r


def search_and_convert_to_json(se_terms, return_type, iters):
    x = []
    se = [search_handler(i, return_type, iters) for i in se_terms]
    for item in se:
        for i in item:
            j = json.loads(i.text)
            x.append(j)
    return (x)


def se_to_json_to_playlist_ids(se_terms, return_type, iters):
    j = search_and_convert_to_json(se_terms, return_type, iters)
    playlist_ids = []
    for i in j:
        try:
            playlists = i["playlists"]
            for i in playlists["items"]:
                owner = i["owner"]
                user_id = owner["id"]
                playlist_ids.append([i["id"], user_id])
        except Exception:
            pass
    return (playlist_ids)


def playlist_ids_to_tracks(playlist_ids_and_user):
    x = []
    for playlist in playlist_ids_and_user:
        playlist_id, playlist_owner = str(playlist[0]), str(playlist[1])
        payload = "https://api.spotify.com/v1/users/" + playlist_owner + "/playlists/" + playlist_id + "/tracks"
        try:
            r = payload_injection_slow(payload)
            x.append(r)
        except Exception:
            pass
    return(x)