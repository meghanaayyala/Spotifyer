#necessary imports
import os
import requests
import spotipy
import base64
import json
# To access authorised Spotify data
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import datetime

######## CHANGE THESE VALUES ###########
client_id = ""
client_secret = ""





# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{client_id}:{client_secret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')
headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

# Obtaining the token for accessing API
token = r.json()['access_token']





def get_meta(songname, artistname, search_type="track"): 
    #getting trackid and artist id from user input of song name and artist name
    headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer { token}"}
    # using the  search API at https://developer.spotify.com/documentation/web-api/reference/search/search/
    search_url = "https://api.spotify.com/v1/search?"
    query=songname+' '+artistname
    data = {"q": query, "type": search_type.lower()}
    from urllib.parse import urlencode
    search_url_formatted = urlencode(data)
    search_r = requests.get(
        search_url+search_url_formatted, headers=headers)
    if search_r.status_code not in range(200, 299):
        print("Encountered issue")
    resp = search_r.json()
    all = []
    for i in range(len(resp['tracks']['items'])):
        track_name = resp['tracks']['items'][i]['name']
        track_id = resp['tracks']['items'][i]['id']
        artist_name = resp['tracks']['items'][i]['artists'][0]['name']
        artist_id = resp['tracks']['items'][i]['artists'][0]['id']
        raw = [track_name, track_id, artist_name, artist_id]
        all.append(raw)

    return all



def get_reccomended_songs(limit, seed_artists, seed_tracks, seed_genres):  # reccomendations API
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    all_recs = []
    query = f'{endpoint_url}limit={limit}&seed_genres={seed_genres}'
    query += f'&seed_artists={seed_artists}'
    query += f'&seed_tracks={seed_tracks}'
    response = requests.get(query, headers={ "Content-type": "application/json", "Authorization": f"Bearer {token}"})
    json_response = response.json()
    if response:
        print("Reccomended songs")
        for i, j in enumerate(json_response['tracks']):
            track_name = j['name']
            artist_name = j['artists'][0]['name']
            link = j['external_urls']['spotify']

            print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")
            reccs = [track_name, artist_name, link]
            all_recs.append(reccs)
        return all_recs