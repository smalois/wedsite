from django.core.management.base import BaseCommand, CommandError
from django.db import transaction 

import spotipy
import spotipy.oauth2 as oauth2

from songpoll.models import Song

class Command(BaseCommand):
    help = 'Seed the database with all the songs from the playlist'

    def get_playlist_tracks(self, playlist_link):
        #Spotify api auth
        # TODO Hide this info
        pub_key = "3b315178fdc04cdd90b2f31a99e787a8"
        priv_key = "32bc18758d704003842f75a7319ce716"
        ccm = oauth2.SpotifyClientCredentials(pub_key, priv_key)
        sp = spotipy.Spotify(client_credentials_manager=ccm)

        username = playlist_link.split('/')[4]
        playlist_id = playlist_link.split('/')[6].split('?')[0]
        
        try:
            results = sp.user_playlist_tracks(username, playlist_id)
        except:
            print('Copy the playlist link', 
                  'Open Spotify and get the playlist link in the sharing options')
            return
        tracks = results['items']
        #THis loop is required to bypass 100 track per list limit
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks

    @transaction.atomic
    def save_playlist_to_db(self, playlist):
        for track in playlist:
            new_song = Song(song_id=track['track']['id'], 
                            artist_name=track['track']['artists'][0]['name'], 
                            name=track['track']['name'], 
                            length_ms=track['track']['duration_ms'])
            new_song.save()
        

    def handle(self, *args, **options):
        playlist_url = "https://open.spotify.com/user/123956110/playlist/6hRfZ6J0nwffuPzYD1V3DS?si=N1U6DBRyR1iYHEv0j10KOA"
        playlist = self.get_playlist_tracks(playlist_url)
        self.save_playlist_to_db(playlist)
