import spotipy
#from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from application.iso_country_codes import CC
from application.models import *
from sqlalchemy import exc
from datetime import datetime
# from iso_country_codes import CC # when no executing Flask

scope = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))



def get_countries_from_spotify():
    list_countries = sp.available_markets()
    return list_countries['markets']

def get_artists_from_spotify():
    scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    artists = sp.current_user_top_artists(limit=20)
    result = []
    
    print(type(artists['items']))
    

    # for a in artists['items']:
    #     print(a['id'], a['name'])

    while artists:
        for idx, artist in enumerate(artists['items']):
            result.append(artist)
        if artists['next']:
            artists = sp.next(artists)
        else:
            artists = None
    
    return result

def get_albums_from_artists(id_list):
    list_albums = []

    if len(id_list) != 0:
        for artist_id in id_list:
            albums_list = sp.artist_albums(artist_id, limit=3)
            for alb in albums_list['items']:
                alb['artists'][0]['id'] = artist_id
                #list_albums.append( (alb, artist_id) )
                if '-' not in alb['release_date']:
                    alb['release_date'] = datetime( int(alb['release_date']), 1, 1 )
                    print(alb['release_date'])
                list_albums.append( alb )
                
    
    return list_albums

def get_tracks_from_albums(id_list):
    list_tracks = []

    if len(id_list) != 0:
        for album_id in id_list:
            tracks_from_album = sp.album_tracks(album_id, limit=12)
            for tr in tracks_from_album['items']:
                tr['album_id'] = album_id
                list_tracks.append( tr )
    
    return list_tracks

def get_my_user():
    scope = "user-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    my_user = sp.current_user()

    return my_user

def get_playlists_from_users(id_list, max=2):
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    result = []

    if len(id_list) != 0:
        for user_id in id_list:
            # For now there's just one user.
            # Counter of playlists
            count = 0

            playlists_from_user = sp.current_user_playlists(limit=max)
            
            #while playlists_from_user:
            for pl in playlists_from_user['items']:
                pl['user_id'] = user_id # Adding user_id attribute
                result.append(pl)
                #print(pl)
                #print(pl['id'], pl['name'], pl['collaborative'])
    return result

def get_playlist_items(playlist_id):
    return sp.playlist_items(playlist_id)

def get_artist_sp(artist_id):
    return sp.artist(artist_id)

def get_album_sp(album_id):
    return sp.album(album_id)

if __name__ == '__main__':
    # c = get_countries_from_spotify()
    # for idx, country in enumerate(c):
    #     print(idx, country)

    # a = get_artists_from_spotify()
    # for idx, art in enumerate(a):
    #     print(idx, art['followers']['total'])

    id_list = []