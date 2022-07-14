from application import app
from flask import jsonify, request
from application.spotipy_methods import *
from application.models import *
from application.iso_country_codes import CC

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
            print(alb['name'])

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
# ALBUM MISSING API METHODS...  

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
            print(tr['name'], tr['album_id'])
           

            id = tr['id']
            name = tr['name']
            #popularity = tr['popularity']
            album_id = tr['album_id']
            album = Album.query.get(album_id)
            artist_id = album.artist_id
            

            new_track = Track(id, name, album_id, artist_id)

            db.session.add(new_track)
            db.session.commit()

        return 'yay'

    
# # Read one
# @app.route('/artists/<id>', methods=['GET'])
# def get_artist(id):
#     artist = Artist.query.get(id)
#     return artist_schema.jsonify(artist)
# # Update one
# @app.route('/artists/<id>', methods=['PUT'])
# def update_artist(id):
#     # Get artist
#     artist = Artist.query.get(id)

#     name = request.json['name']
#     url = request.json['url']
#     followers = request.json['followers']

#     # Update python class
#     artist.name = name
#     artist.url = url
#     artist.followers = followers

#     # Update on DB
#     db.session.commit()

#     return artist_schema.jsonify(artist)
# # Delete one
# @app.route('/artists/<id>', methods=['DELETE'])
# def delete_artist(id):
#     # Get artist
#     artist = Artist.query.get(id)
#     # Delete that artist
#     db.session.delete(artist)

#     # Commit that change
#     db.session.commit()

#     return artist_schema.jsonify(artist)

