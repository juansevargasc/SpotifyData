from app import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    followers = db.Column(db.Integer)

    def __init__(self, name, url, followers):
        self.name = name
        self.url = url
        self.followers = followers
        