import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

artist_name = []
track_name = []
popularity = []
track_id = []


for i in range(0,10000,50):
    f = open(('search2021') + '.txt', 'a', encoding='utf-8')
    track_results = sp.search(q='year:2021', type='track', limit=50, offset=i)
    for j, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
        line = f"{j}, {t['artists'][0]['name']}, {t['name']}, {t['id']}, {t['popularity']}\n"
        f.write(line)
    f.close()
# https://open.spotify.com/artist/4gzpq5DPGxSnKTe4SA8HAU?si=4mmEtJ1YQCmNdNo0GsaXlw