from SmartGlovesProject_Server.Data_Prepare import credential as cred
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

if __name__ == '__main__':
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cred.client_ID,client_secret=cred.client_SECRET))
    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()