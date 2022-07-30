from pyparsing import FollowedBy
from application import app
from flask import jsonify, request
from application.spotipy_methods import *
from application.models import *
from application.iso_country_codes import CC
from datetime import datetime

# ROUTES
# Health - ping tests
@app.route('/ping')
def ping_route():
    db.engine.execute('SELECT 1')
    return ''

# Testing get request
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'msg': 'Hello World'})



# ARTIST
# Create
@app.route('/artists', methods=['POST'])
def add_artist():
    id = request.json['id']
    name = request.json['name']
    image_url = request.json['image_url']
    followers = request.json['followers']

    new_artist = Artist(id, name, image_url, followers)

    db.session.add(new_artist)
    db.session.commit()


    return artist_schema.jsonify(new_artist)
# Read all
@app.route('/artists', methods=['GET'])
def get_artists():
    if len( Artist.query.all() ) != 0:
        all_artists = Artist.query.all()

        # ! UPDATING Artist First track once it is on DB ! #
        if len( Track.query.all() ) != 0:
            for art in all_artists:
                list_tracks = get_artist_top_tracks(art.id)

                # If there's already tracks on DB
                if list_tracks is not None:
                    
                    for i in range(5):
                        first_track = list_tracks[i]
                        track = Track.query.get(first_track['id'])

                        if track is not None:
                            # Update popularity
                            track.popularity = first_track['popularity']
                            db.session.commit()
                        else:
                            # if track is None:
                            id = first_track['id']
                            name = first_track['name']
                            popularity = first_track['popularity']
                            alb_id = first_track['album']['id']
                            album = Album.query.get(alb_id)
                            if album is not None:
                                album_id = album.id
                            else:
                                album_id = None
                            artist_id = art.id

                            new_track = Track(id, name, album_id, artist_id, popularity)

                            # # Adding all markets to this track
                            # for country_code in first_track['available_markets']:
                            #     # Look for country in DB
                            #     country = Country.query.filter_by(code=country_code).first()
                                
                            #     if country is not None:
                            #         new_track.countries.append(country)

                            db.session.add(new_track)
                            db.session.commit()


        result = artists_schema.dump(all_artists)
        return jsonify(result)
    else:
        artists = get_artists_from_spotify()
        for idx, artist in enumerate(artists):
            id = artist['id']
            name = artist['name']
            image_url = artist['images'][0]['url']
            followers = artist['followers']['total']

            # print(idx, a)

            new_artist = Artist(id, name, image_url, followers)

            db.session.add(new_artist)
            db.session.commit()
        return 'Success'

# Read one
@app.route('/artists/<id>', methods=['GET'])
def get_artist(id):
    artist = Artist.query.get(id)
    return artist_schema.jsonify(artist)



# Update one
@app.route('/artists/<id>', methods=['PUT'])
def update_artist(id):
    # Get artist
    artist = Artist.query.get(id)

    name = request.json['name']
    image_url = request.json['image_url']
    followers = request.json['followers']

    # Update python class
    artist.name = name
    artist.image_url = image_url
    artist.followers = followers

    # Update on DB
    db.session.commit()

    return artist_schema.jsonify(artist)
# Delete one
@app.route('/artists/<id>', methods=['DELETE'])
def delete_artist(id):
    # Get artist
    artist = Artist.query.get(id)
    # Delete that artist
    db.session.delete(artist)

    # Commit that change
    db.session.commit()

    return artist_schema.jsonify(artist)

#COUNTRY
# Create
@app.route('/countries', methods=['POST'])
def add_country():
    id = request.json['id']
    code = request.json['code']
    name = request.json['name']

    new_country = Country(id, code, name)

    db.session.add(new_country)
    db.session.commit()


    return country_schema.jsonify(new_country)

# Read all
@app.route('/countries', methods=['GET'])
def get_countries():
    if len( Country.query.all() ) != 0:
        all_countries = Country.query.all()
        result = countries_schema.dump(all_countries)

        return jsonify(result)
    else:
        countries = get_countries_from_spotify()
        for idx, country in enumerate(countries):
            id = idx
            code = country
            name = CC[code]

            new_coutry = Country(id, code, name)

            db.session.add(new_coutry)
            db.session.commit()
        return 'Success'

# Read One
@app.route('/countries/<id>', methods=['GET'])
def get_country(id):
    country = Country.query.get(id)
    return country_schema.jsonify(country)
# Update one
@app.route('/countries/<id>', methods=['PUT'])
def update_country(id):
    # Get country
    country = Country.query.get(id)

    code = request.json['code']
    name = request.json['name']

    # Update python class
    country.code = code
    country.name = name
    

    # Update on DB
    db.session.commit()

    return country_schema.jsonify(country)
# Delete one
@app.route('/countries/<id>', methods=['DELETE'])
def delete_country(id):
    # Get country
    country = Country.query.get(id)
    # Delete that artist
    db.session.delete(country)

    # Commit that change
    db.session.commit()

    return country_schema.jsonify(country)
    

# ALBUM 
# Create
@app.route('/albums', methods=['POST'])
def add_album():
    id = request.json['id']
    name = request.json['name']
    total_tracks = request.json['total_tracks']
    album_type = request.json['album_type']
    spotify_url = request.json['spotify_url']
    image_url = request.json['image_url']
    release_date = request.json['release_date']
    artist_id = request.json['artist_id']

    new_album = Album(id, name, total_tracks, album_type, spotify_url, image_url, release_date, artist_id)

    db.session.add(new_album)
    db.session.commit()

    return album_schema.jsonify(new_album)
# # Read all
@app.route('/albums', methods=['GET'])
def get_albums():
    if len( Album.query.all() ) != 0:
        all_albums = Album.query.all()
        result = albums_schema.dump(all_albums)
        
        return jsonify(result)

    else:
        all_artists = Artist.query.all()
        id_list = [ art.id for art in all_artists ]
        list_albums = get_albums_from_artists(id_list)
        
        
        for alb in list_albums:
            #print(alb['name'])

            id = alb['id']
            name = alb['name']
            total_tracks = alb['total_tracks']
            album_type = alb['album_type']
            spotify_url = alb['external_urls']['spotify']
            image_url = alb['images'][0]['url']
            release_date = alb['release_date']
            artist_id = alb['artists'][0]['id']

            new_album = Album(id, name, total_tracks, album_type, spotify_url, image_url, release_date, artist_id)

            db.session.add(new_album)
            db.session.commit()

        return 'yay'
# Read One
@app.route('/albums/<id>', methods=['GET'])
def get_album(id):
    album = Album.query.get(id)
    return album_schema.jsonify(album)
# Update one
@app.route('/albums/<id>', methods=['PUT'])
def update_album(id):
    # Get album
    album = Album.query.get(id)

    name = request.json['name']
    total_tracks = request.json['total_tracks']
    album_type = request.json['album_type']
    spotify_url = request.json['spotify_url']
    image_url = request.json['image_url']
    release_date = request.json['release_date']
    artist_id = request.json['artist_id']

    # Update python class
    album.name = name
    album.total_tracks = total_tracks
    album.album_type = album_type
    album.spotify_url = spotify_url
    album.image_url = image_url
    album.release_date = release_date
    album.artist_id = artist_id

    

    # Update on DB
    db.session.commit()

    return album_schema.jsonify(album)
# Delete one
@app.route('/albums/<id>', methods=['DELETE'])
def delete_album(id):
    # Get album
    album = Album.query.get(id)
    # Delete that artist
    db.session.delete(album)

    # Commit that change
    db.session.commit()

    return album_schema.jsonify(album)

# TRACKS
# Create
@app.route('/tracks', methods=['POST'])
def add_track():
    id = request.json['id']
    name = request.json['name']
    popularity = request.json['popularity']
    album_id = request.json['album_id']
    artist_id = request.json['artist_id']

    new_track = Track(id, name, popularity, album_id, artist_id)

    db.session.add(new_track)
    db.session.commit()

    return track_schema.jsonify(new_track)
# # Read all
@app.route('/tracks', methods=['GET'])
def get_tracks():
    if len( Track.query.all() ) != 0:
        all_tracks = Track.query.all()
        result = tracks_schema.dump(all_tracks)

        return jsonify(result)

    else:
        all_albums = Album.query.all()
        id_list = [ alb.id for alb in all_albums ]
        list_tracks = get_tracks_from_albums(id_list)
        
        
        for tr in list_tracks:
            #print(tr['name'], tr['album_id'])
            #track = Track.query.get(tr['id'])

            # if track is None:
            id = tr['id']
            name = tr['name']
            #popularity = tr['popularity']
            album_id = tr['album_id']
            album = Album.query.get(album_id)
            artist_id = album.artist_id

            new_track = Track(id, name, album_id, artist_id)

            # Adding all markets to this track
            for country_code in tr['available_markets']:
                # Look for country in DB
                country = Country.query.filter_by(code=country_code).first()
                
                if country is not None:
                    new_track.countries.append(country)

            db.session.add(new_track)
            db.session.commit()

        return 'yay'
# Read One
@app.route('/tracks/<id>', methods=['GET'])
def get_track(id):
    track = Track.query.get(id)
    return track_schema.jsonify(track)
#
@app.route('/tracks/update-popularity', methods=['GET'])
def get_popularity():
    # Fetch ALL tracks
    all_tracks = Track.query.all()
    
    # Go through all tracks updating its
    for track in all_tracks:
        if track.popularity == 0:
            # Get track info from Spotify
            track_sp = get_track_sp(track.id)
            if track_sp is not None:
                # Udate the track popularity and commit
                track.popularity = track_sp['popularity']
                print('Track Updated', track)
                db.session.commit()
    return 'Perfect'


# Update one
@app.route('/tracks/<id>', methods=['PUT'])
def update_track(id):
    # Get track
    track = Track.query.get(id)

    name = request.json['name']
    popularity = request.json['popularity']
    album_id = request.json['album_id']
    artist_id = request.json['artist_id']

    # Update python class
    track.name = name
    track.popularity = popularity
    track.album_id = album_id
    track.artist_id = artist_id

    # Update on DB
    db.session.commit()

    return track_schema.jsonify(track)
# Delete one
@app.route('/tracks/<id>', methods=['DELETE'])
def delete_track(id):
    # Get track
    track = Track.query.get(id)
    # Delete that artist
    db.session.delete(track)

    # Commit that change
    db.session.commit()

    return track_schema.jsonify(track)


# PLAYLISTS
# Create
@app.route('/playlists', methods=['POST'])
def add_playlist():
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    followers = request.json['followers']
    image_url = request.json['image_url']
    collaborative = request.json['collaborative']
    user_id = request.json['user_id']

    new_playlist = Playlist(id, name, description, followers, image_url, collaborative, user_id)

    db.session.add(new_playlist)
    db.session.commit()

    return playlist_schema.jsonify(new_playlist)  
# Read one
@app.route('/playlists/<id>', methods=['GET'])
def get_playlist(id):
    playlist = Playlist.query.get(id)
    return playlist_schema.jsonify(playlist)
# # Read all
@app.route('/playlists', methods=['GET'])
def get_playlists():
    if len( Playlist.query.all() ) != 0:
        all_playlists = Playlist.query.all()
        result = playlists_schema.dump(all_playlists)

        return jsonify(result)

    else: ## to implement
        all_users = User.query.all()
        id_list = [ usr.id for usr in all_users ]
        list_playlists = get_playlists_from_users(id_list, max=12)
        

        # 1. We start iterating all playlists
        count = 0 # Counter of playlists
        for pl in list_playlists:
            
            id = pl['id']
            name = pl['name']
            description = pl['description']
            followers = pl['tracks']['total']
            image_url = pl['images'][0]['url']
            collaborative = pl['collaborative']
            user_id = pl['user_id']

            new_playlist = Playlist(id, name, description, followers, image_url, collaborative, user_id)


            tracks_of_playlist = get_playlist_items(pl['id'])
            count_tracks = 0
            for track_pl in tracks_of_playlist['items']:
                
                #print('track album:', track_pl['track']['album']['name'])
                try:
                    # Try Query
                    track_db = Track.query.get(track_pl['track']['id'])
                    if track_db is None:
                        #print(track_pl['track']['name'])
                        #print('Artist' , track_pl['track']['artists'][0]['name'])
                        
                        # Check if Artist Exists, if not, it adds it to the DB as anew object.
                        artist_db = Artist.query.get(track_pl['track']['artists'][0]['id'])
                        if artist_db is None:
                            artist = get_artist_sp(artist_id=track_pl['track']['artists'][0]['id'])
                            # Parameters
                            id = artist['id']
                            name = artist['name']
                            image_url = artist['images'][0]['url']
                            followers = artist['followers']['total']

                            new_artist = Artist(id, name, image_url, followers)
                            db.session.add(new_artist)
                            db.session.commit()
                            #print('Artist: ', artist['name'])
                        count_tracks += 1

                        # Check if Album Exists, if not, it adds it to the DB as a new object.
                        album_db = Album.query.get(track_pl['track']['album']['id'])
                        if album_db is None:
                            alb = get_album_sp(album_id=track_pl['track']['album']['id'])

                            id = alb['id']
                            name = alb['name']
                            total_tracks = alb['total_tracks']
                            album_type = alb['album_type']
                            spotify_url = alb['external_urls']['spotify']
                            image_url = alb['images'][0]['url']
                            release_date = alb['release_date']
                            artist_id = track_pl['track']['artists'][0]['id'] # The album may be from another artists sharing the song

                            # Check Date
                            if '-' not in alb['release_date']:
                                release_date = datetime( int(alb['release_date']), 1, 1 )
                                print(alb['release_date'])

                            new_album = Album(id, name, total_tracks, album_type, spotify_url, image_url, release_date, artist_id)

                            #print('Album: ', name)
                            db.session.add(new_album)
                            db.session.commit()

                        # Now that we're confident Artist and Album exists on DB! we can create our new track object :)
                        artist_id = track_pl['track']['artists'][0]['id']
                        album_id = track_pl['track']['album']['id']
                        id = track_pl['track']['id']
                        name = track_pl['track']['name']

                        new_track = Track(id, name, album_id, artist_id)

                        # Adding all markets to this track
                        for country_code in track_pl['track']['available_markets']:
                            # Look for country in DB
                            country = Country.query.filter_by(code=country_code).first()
                            
                            if country is not None:
                                new_track.countries.append(country)

                        db.session.add(new_track)
                        db.session.commit()

                        # Associate Track with Playlist m-m
                        new_playlist.tracks.append(new_track)
                        #print('Track!:', name)
                    else:
                        print('EXIST ALREADY ON DB')
                        # Associate Track with Playlist m-m
                        new_playlist.tracks.append(track_db)
                    
                    

                except exc.SQLAlchemyError as e:
                    print(type(e))
            print('Total tracks: ', count_tracks)

            count += 1
            print('Count', count)

            # Finally ADD PLAYLIST ON DB!!
            db.session.add(new_playlist)
            db.session.commit()

        ##
        return 'Success'
        
    
# Update one
@app.route('/playlists/<id>', methods=['PUT'])
def update_playlist(id):
    # Get playlist
    playlist = Playlist.query.get(id)

    name = request.json['name']
    description = request.json['description']
    followers = request.json['followers']
    image_url = request.json['image_url']
    collaborative = request.json['collaborative']
    user_id = request.json['user_id']

    # Update python class
    playlist.name = name
    playlist.description = description
    playlist.followers = followers
    playlist.image_url = image_url
    playlist.collaborative = collaborative
    playlist.user_id = user_id

    # Update on DB
    db.session.commit()

    return playlist_schema.jsonify(playlist)
# Delete one
@app.route('/playlists/<id>', methods=['DELETE'])
def delete_playlist(id):
    # Get playlist
    playlist = Playlist.query.get(id)
    # Delete that artist
    db.session.delete(playlist)

    # Commit that change
    db.session.commit()

    return playlist_schema.jsonify(playlist)


# USER
# Create
@app.route('/users', methods=['POST'])
def add_user():
    id = request.json['id']
    display_name = request.json['display_name']
    followers = request.json['followers']
    image_url = request.json['image_url']
    product_type = request.json['product_type']
    country_id = request.json['country_id']

    new_user = User(id, display_name, followers, image_url, product_type, country_id)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)  
# Read one
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)
# # Read all
@app.route('/users', methods=['GET'])
def get_users():
    if len( User.query.all() ) != 0:
        all_users = User.query.all()
        result = users_schema.dump(all_users)

        return jsonify(result)

    else:
        current_user = get_my_user()
        current_user_followed_art_list = get_current_user_followed_artists()
    
        # New User Info
        id = current_user['id']
        display_name = current_user['display_name']
        followers = current_user['followers']['total']
        image_url = current_user['images'][0]['url']
        product_type = current_user['product']
        # Which country. SQLAlchemy query
        country = Country.query.filter_by(code=current_user['country']).first()
        country_id = country.id

        new_user = User(id, display_name, followers, image_url, product_type, country_id)

        # Adding artists on DB, to many - many User - Artist
        for artist_in_list in current_user_followed_art_list:
            artist = Artist.query.get(artist_in_list['id'])

            if artist is not None:
                new_user.artists.append(artist)
            else:
                new_artist = get_artist_sp(artist_in_list['id'])
                
                id = new_artist['id']
                name = new_artist['name']
                image_url = new_artist['images'][0]['url']
                followers = new_artist['followers']['total']

                # print(idx, a)

                new_artist = Artist(id, name, image_url, followers)


                # Adding relationship many to many
                new_user.artists.append(new_artist)

                # Adding artist that was not on DB.
                db.session.add(new_artist)
                db.session.commit()


        db.session.add(new_user)
        db.session.commit()

        return 'User succesfully added'
        

# Update one
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    # Get user
    user = User.query.get(id)

    display_name = request.json['display_name']
    followers = request.json['followers']
    image_url = request.json['image_url']
    product_type = request.json['product_type']
    country_id = request.json['country_id']

    # Update python class
    user.display_name = display_name
    user.followers = followers
    user.image_url = image_url
    user.product_type = product_type
    user.country_id = country_id

    # Update on DB
    db.session.commit()

    return user_schema.jsonify(user)
    
# Delete one
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    # Get user
    user = User.query.get(id)
    # Delete that artist
    db.session.delete(user)

    # Commit that change
    db.session.commit()

    return user_schema.jsonify(user)