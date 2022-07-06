from application import *

# MODELS and SCHEMAS
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name

class CountrySchema(ma.Schema):
    class Meta:
        fields = ('id', 'code', 'name')
#
class Artist(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(200))
    followers = db.Column(db.Integer)

    def __init__(self, id, name, image_url, followers):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.followers = followers

class ArtistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'image_url', 'followers')
#
class Album(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100))
    total_tracks = db.Column(db.Integer)
    album_type = db.Column(db.String(100))
    spotify_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    release_date = db.Column(db.DateTime(timezone=True))


    def __init__(self, id, name, total_tracks, album_type, spotify_url, image_url, release_date):
        self.id = id
        self.name = name
        self.total_tracks = total_tracks
        self.album_type = album_type
        self.spotify_url = spotify_url
        self.image_url = image_url
        self.release_date = release_date

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'total_tracks', 'album_type', 'spotify_url', 'image_url')
#
class Playlist(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    followers = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    collaborative = db.Column(db.Boolean)


    def __init__(self, id, name, description, followers, image_url, collaborative):
        self.id = id
        self.name = name
        self.description = description
        self.followers = followers
        self.image_url = image_url
        self.collaborative = collaborative

class PlaylistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'followers', 'image_url', 'collaborative')
#
class User(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    display_name = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    product_type = db.Column(db.String(100))

    def __init__(self, id, display_name, followers, image_url, product_type):
        self.id = id
        self.display_name = display_name
        self.followers = followers
        self.image_url = image_url
        self.product_type = product_type

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'display_name', 'followers','image_url', 'product_type')
#
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    popularity = db.Column(db.String(200))

    def __init__(self, id, name, popularity):
        self.id = id
        self.name = name
        self.popularity = popularity

class TrackSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'popularity')
#

# SCHEMAS
# Init SchemaS

# Country
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
# Artist
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
# Album
album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)
# Playlist
playlist_schema = PlaylistSchema()
playlists_schema = PlaylistSchema(many=True)
# User
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# Track
track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)
