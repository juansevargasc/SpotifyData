from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from search import *

# Init App
app = Flask(__name__)

# SETUP
# Init Daabase
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hcbkgsjxeesuic:e6a05215cbf2a0454e1216744ad29621b462699a6fa21eddf8959403a641a748@ec2-44-206-214-233.compute-1.amazonaws.com/d7orsoge8mf86g'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://juansevargas:postgres@localhost/SpotifyService'
#jdbc:postgresql:localhost:5432/SpotifyService
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'juansevargas'

 # Init DB
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

from application import routes