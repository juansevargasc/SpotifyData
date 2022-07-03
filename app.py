from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#from artist import Artist

# Init App
app = Flask(__name__)

# Init Daabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://juansevargas:juansevargas@localhost/SpotifyService'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'juansevargas'

# Init DB
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    followers = db.Column(db.Integer)

    def __init__(self, name, url, followers):
        self.name = name
        self.url = url
        self.followers = followers

class ArtistSchema(ma.Schema):
    class Meta:
        #fields = (Artist.id, Artist.name, Artist.url, Artist.followers)
        fields = ('id', 'name', 'url', 'followers')

# Init Schema
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)



# TESTING GET REQUEST
# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({'msg': 'Hello World'})

@app.route('/health')
def health():
    return "health"

@app.route('/artist', methods=['POST'])
def add_artist():
    name = request.json['name']
    url = request.json['url']
    followers = request.json['followers']

    new_artist = Artist(name, url, followers)

    db.session.add(new_artist)
    db.session.commit()

    return artist_schema.jsonify(new_artist)

@app.route('/artist', methods=['GET'])
def get_products():
    all_artists = Artist.query.all()
    result = artists_schema.dump(all_artists)

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
    #db.create_all()