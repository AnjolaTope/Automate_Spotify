
import  os

import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import  youtube_dl


#This is a Playlist class that takes the id of a playlists and its name 
class Playlist(object):
     def __init__(self, id, title):
        self.id = id
        self.title = title 

#This is a Song class that takes the name of the song and the name of the playlist 
class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track 

#This class is where we Interact with the youtube and gets the required data 
class YoutubeClient(object):
    def __init__(self,credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build( api_service_name, api_version, credentials=credentials)
        self.youtube_client = youtube_client
        
        
    #This fucntion gets our playlist form youtube
    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            #get id of the playlist
            #in part we say what data we wont from each playlist 
            part="id, snippet",

            #tell youtube the maximum number of playlists we want
            maxResults=50,
          
            #ensures we get out own playlist not someone else
            mine= True
        )

        response= request.execute()
        #print(response)
        #playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists



        


# this function gets the videos from the playlist
    def get_videos_from_playlist(self,playlist_id):
        songs=[]
        request = self.youtube_client.playlistItems().list(
            #gets the playloist id 
            playlistId = playlist_id,

            #in part we say what data we wont from each playlist 
            part = 'id, snippet',

            #tell youtube the maximum number of songs we want
            maxResults = 50
        )

        response= request.execute()


        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']

            artist, track = self.get_artist_and_track_from_video(video_id)
            if artist and track:
                songs.append(Song(artist, track))

        return  songs
        


#we used the name of the artists and the name of the song 
    def get_artist_and_track_from_video(self,video_id):
        #this is the youtube url for the video 
        #youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        #this gets data of the song from the youtube data library 
        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download =False
        )

        # stores the name of the artists from the data libraary 
        artist =  video['artist']

        # stores the name of the track  from the data libraary 
        track = video['track']


        return artist, track


    