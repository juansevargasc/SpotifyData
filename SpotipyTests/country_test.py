import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

list_of_countries = sp.available_markets()

def get_countries():
    # for idx, country in enumerate(list_of_countries['markets']):
    #     print(idx, country)
    return list_of_countries['markets']

