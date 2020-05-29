import os

from youtube_client import YoutubeClient
from spotify_client import SpotifyClient

def run():
    os.environ['SPOTIFY_AUTH_TOKEN'] = 'put spotify token here '
    
    # Get a list of our playlists from youtube
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



