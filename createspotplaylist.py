import json
import os
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from exceptions import ResponseException
from secrets import spotify_token,spotify_user_id



class CreatePlaylist:
    def __init__(self):
        #self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}


    def get_artist_tracks(self):
        df=pd.read_csv('artisttrack.csv')
        artists_list = df['artist'].tolist()
        tracks_list = df['track'].tolist()
        for artist, song_name in zip(artists_list, tracks_list): 
            if song_name is not None and artist is not None:
                # save all important info and skip any missing song and artist
                video_title=artist+" "+song_name
                if(self.get_spotify_uri(song_name,artist) is not None):
                    self.all_song_info[video_title] = {
                        # add the uri, easy to get song to put into playlist
                            "spotify_uri": self.get_spotify_uri(song_name, artist),
                            "song_name": song_name,
                            "artist": artist,

                    }

    def create_playlist(self):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": "Reddit Top Posts",
            "description": "All Top Posts Songs",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        # playlist id
        try:
            response_json = response.json()
        except Exception:
            return None
        return response_json.get('id', None)
            #return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        
        songs = response_json["tracks"]["items"]
        
        # only use the first song
        if(len(songs)<1):
            return None
        uri = songs[0]["uri"]
        #print(uri)
        return uri

    def add_song_to_playlist(self):
        """Add all liked songs into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.get_artist_tracks()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()