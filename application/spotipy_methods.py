import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from application.iso_country_codes import CC

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)



def get_countries_from_spotify():
    # for idx, country in enumerate(list_of_countries['markets']):
    #     print(idx, country)
    list = sp.available_markets()
    return list['markets']



if __name__ == '__main__':
    countries = get_countries_from_spotify()
    for idx, country in enumerate(countries):
        print(idx, country, CC[country])