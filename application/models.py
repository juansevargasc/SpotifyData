from application import *

# MODELS and SCHEMAS

#INTERMEDIATE TABLES - FOR MANY TO MANY RELATIONSHIPS
track_playlist = db.Table('track_playlist',
    db.Column('track_id', db.String(200), db.ForeignKey('track.id'), primary_key=True),
    db.Column('playlist_id', db.String(200), db.ForeignKey('playlist.id'), primary_key=True)
)

country_track = db.Table('country_track',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id')),
    db.Column('track_id', db.String(200), db.ForeignKey('track.id'))
)
user_artist = db.Table('user_artist',
    db.Column('user_id', db.String(200), db.ForeignKey('user.id')),
    db.Column('artist_id', db.String(200), db.ForeignKey('artist.id'))
)
#

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))

    users = db.relationship('User', backref='country', lazy=True) # Relationship

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

    albums = db.relationship('Album', backref='artist', lazy=True) # Relationship
    tracks = db.relationship('Track', backref='artist', lazy=True) # Relationship

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
    name = db.Column(db.String(400))
    total_tracks = db.Column(db.Integer)
    album_type = db.Column(db.String(100))
    spotify_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    release_date = db.Column(db.DateTime(timezone=True))
    #tracks = db.relationship('Track', backref='album', lazy=True) # One to many relationship
    artist_id = db.Column(db.String(200), db.ForeignKey('artist.id'), nullable=True) # ForeignKey Artist
    
    tracks = db.relationship('Track', backref='album', lazy=True) # One to many relationship
    
    def __init__(self, id, name, total_tracks, album_type, spotify_url, image_url, release_date, artist_id):
        self.id = id
        self.name = name
        self.total_tracks = total_tracks
        self.album_type = album_type
        self.spotify_url = spotify_url
        self.image_url = image_url
        self.release_date = release_date
        self.artist_id = artist_id

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'total_tracks', 'album_type', 'spotify_url', 'image_url', 'artist_id')
#
class Playlist(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    followers = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    collaborative = db.Column(db.Boolean)
    user_id = db.Column(db.String(200), db.ForeignKey('user.id'), nullable=True) # ForeignKey User

    tracks = db.relationship('Track', secondary=track_playlist, backref='playlists') # Many to many

    def __init__(self, id, name, description, followers, image_url, collaborative, user_id):
        self.id = id
        self.name = name
        self.description = description
        self.followers = followers
        self.image_url = image_url
        self.collaborative = collaborative
        self.user_id = user_id

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
    country_id = db.Column(db.Integer, db.ForeignKey('country.id')) # ForeignKey User

    playlists = db.relationship('Playlist', backref='user', lazy=True) # One to many relationship
    artists = db.relationship('Artist', secondary=user_artist, backref='users') # Many to Many

    def __init__(self, id, display_name, followers, image_url, product_type, country_id):
        self.id = id
        self.display_name = display_name
        self.followers = followers
        self.image_url = image_url
        self.product_type = product_type
        self.country_id = country_id

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'display_name', 'followers','image_url', 'product_type', 'country_id')
#
class Track(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200))
    popularity = db.Column(db.Integer)
    album_id = db.Column(db.String(200), db.ForeignKey('album.id'), nullable=True) # ForeignKey Album
    artist_id = db.Column(db.String(200), db.ForeignKey('artist.id')) # ForeignKey Artist

    countries = db.relationship('Country', secondary=country_track, backref='tracks')

    def __init__(self, id, name, album_id, artist_id, popularity=0):
        self.id = id
        self.name = name
        self.popularity = popularity
        self.album_id = album_id
        self.artist_id = artist_id


class TrackSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'popularity', 'album_id', 'artist_id')
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
