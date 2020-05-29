
import requests
from urllib.parse import urlparse
import urllib.parse



class SpotifyClient(object):

    def __init__(self, api_token):
        #this token is used to issue a request 
        self.api_token = api_token


    def search_song(self, artist, track):
        #this is used to get the url of the string 
        query = urllib.parse.quote(f'{artist} {track}')
        #this specifies that we are searching for a track 
        url = f"http://api.spotify.com/v1/search?q={query}&type=track"
        #make the requests from spotify and gets data wee need 
        response = requests.get(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {self.api_token}"
            }

        )

        #gets reponse as a json file
        response_json = response.json()

        #to get the songs from the response
        results = response_json['tracks']['items']
        if results:
            #we get the id for the first song because this has a higher chance of being the song we want 
            return results[0]['id']
        # if the song is not found    
        else:
             raise Exception(f"No song found for {artist} = {track}")

    def add_song_to_spotify(self, song_id):
        #this is a url that we will issue a request to add the song to a playlist
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )
        


        return response.ok


    

         