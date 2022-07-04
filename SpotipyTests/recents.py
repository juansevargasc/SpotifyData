import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Scope
scope = "user-read-recently-played"

# Setting up
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
f = open(('user_recents') + '.txt', 'a', encoding='utf-8')

results = sp.current_user_recently_played(limit=50)
for idx, item in enumerate(results['items']):
    track = item['track']
    #print(idx, track['artists'][0]['name'], " – ", track['name'])
    f.write(idx, track['artists'][0]['name'], " – ", track['name'])

f.close()