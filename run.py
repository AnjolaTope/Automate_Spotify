import os

from youtube_client import YoutubeClient
from spotify_client import SpotifyClient

def run():
    os.environ['SPOTIFY_AUTH_TOKEN'] = 'BQCYw2XJKN76kjIiA6gJH8E5c_d3WRQBqX74wFTa7UDwYUSc4rJ1AEocQBFPH2LaOK-1ddJcyaa0ZUZ5s4sZO7n_mGT8OgrQZBzbWxyjfn27GPFr-Vs-ULqi0BdYqP-Z4ehb18I-l9YZJeG6_1xNiabqwc4_ON6mKFejO-O2lw'
    #result=os.getenv('SPOTIFY_AUTH_TOKEN')
    #echo print(result)
    
    # Get a list of our playlists from youtube
    #spotify_token = 'BQBE0nNuW57zVmP04CPmuGvwVHofAtusvHbcFR6SqBFsbYXctprM8iWQC_IqQmefd53qTtq_X_RhhQl0iN8PFPm3FLSonz4YxY0HIpF4VrOTMmd88C8XYHT8wlkSRryG8jewiTZ-e-9-UUyza_QCo-9TsVxQA7_S58dyiRImhQ'
    youtube_client = YoutubeClient('./credentials/client_secret.json')
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN'))
    playlists = youtube_client.get_playlists()

    # Ask whcih playlists we want to get the video from
    for index,playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")

    choice = int(input("Enter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")


    # For each video in the playlist, get the song information form youtube 
    songs =youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)} ")


    # Search for the song on spotify
    for song in songs:
        spotify_song_id =  spotify_client.search_song(song.artist,song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print(f" Added {song.artist} ")



    # If we find the song add it to our Spotify liked songs
    
    pass


if __name__ == '__main__':
    run()



