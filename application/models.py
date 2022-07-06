from application import *

# MODELS and SCHEMAS
class Artist(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    followers = db.Column(db.Integer)


    def __init__(self, id, name, url, followers):
        self.id = id
        self.name = name
        self.url = url
        self.followers = followers

class ArtistSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'url', 'followers')

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
        self.release_date
    
#class AlbumSchema


# SCHEMAS
# Init SchemaS

# Artist
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
