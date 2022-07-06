from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from search import *

# Init App
app = Flask(__name__)

# SETUP
# Init Daabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://juansevargas:postgres@localhost/SpotifyService'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'juansevargas'

 # Init DB
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

from application import routes