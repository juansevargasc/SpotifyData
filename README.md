# Data Engineering Starter Project
Python service which provides an API to simulate some Spotify features. It is a system that saves Spotify data on a relational database, and can be accessed through an API. It can be accessed both through the API routes or through a connection to the Database.

### Spotify Service
> Juan Sebastián Vargas C.
> Loka - Data Analyst Intern

## Running the application 
1. First get your Spotify Credentials on https://developer.spotify.com/dashboard/login. Register your app, making note of your **Client ID** and your **App Secret**. If you don't already have a Spotify account, you will need to create one. If you want to know more about the Spotify Web API, check [this article](https://kaylouisebennett.medium.com/getting-started-with-spotifys-web-api-part-1-cff30c1b23ef)

2. Go to the [Docker Compose File](https://github.com/juansevargasc/SpotifyData/blob/main/docker-compose.yml), then go to the `pythonapp` section. Go to `environment` and fill the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` variables, you can leave `SPOTIPY_REDIRECT_URI` as it is.

3. Now go to your terminal and build the containers.
   
```docker-compose build```

4. Now you can run them all detached. 

```docker-compose up -d```

5. Finally, you can run 
`docker-compose exec pythonapp python3 make_pgdb.py`
to create the Database. Now you'll be able to check the database. If you want to reset it you could use `docker-compose exec pythonapp python3 drop_pgdb.py` as well.

You will see three containers:
- The main app called `pythonapp`
- The Postgres Database called `db`
- PGAdmin, the graphical interface running to interact with the database. You can access it going to `http://127.0.0.1:8080` on your browser if you want.
  - User: admin@admin.com, Password: admin.
- If you want to connect the database to PGAdmin or to any other tool such a Dashboard Tool use:
  - **Host**: db  (which is the name of the database container)
  - **User**: spotifyuser
  - **Password**: postgres
  - **Database**: SpotifyDocker

> You can change this configuration on the docker-compose.yml file

### What you will see

First go to the browser or use a tool such as Postman to check the API. Make the `GET` requests in this order (just for the very first time):
   1. Countries
   2. Playlists
   3. Update Tracks Popularity
   
```
http://127.0.0.1:4000/countries
http://127.0.0.1:4000/Playlists
http://127.0.0.1:4000/tracks/update-popularity
```

Then you can use the rest of the routes to pull: tracks, artists, albums, countries and playlists. You can use it as **Backend** service to serve a Frontend side, or you can connect a DataViz tool to create some nice **Visualizations**.

Here you can check some!


### Docker Container
Link to [Docker File](Dockerfile)


### Requirements
```python
# capture requirements to install
pip freeze > requirements.txt

# install requirements from requirements.txt
pip install -r requirements.txt
```

### Environment Variables - Flask
```bash
export FLASK_ENV=development
export FLASK_APP=run.py
```

### Database Migrations in Flask
```python
from application import *

db.drop_all() # If there's updates on Columns or new models, it's necessary to drop the DB
db.create_all() # It'll create the DB.
```

### Tree Structure
```bash
.
├── README.md
├── SpotipyTests
│   ...
├── __pycache__
│   ...
├── application
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── iso_country_codes.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── routes.cpython-39.pyc
│   │   └── spotipy_methods.cpython-39.pyc
│   ├── iso_country_codes.py
│   ├── models.py
│   ├── routes.py
│   └── spotipy_methods.py
├── documents
│   ├── Database ER diagram GENERAL.png
│   ├── Drafts
│   │   ├── Blank diagram - UML Class.pdf
│   │   └── UML-Class Diagram 1.png
│   └── UML Class Diagram.png
├── img
│   ...
├── requirements.txt
├── run.py
└── spotify_playlist.txt

8 directories, 49 files
```

# Description



The source of information is the [Spotify web public API](https://developer.spotify.com/documentation/web-api/). The level of detail and data features are described below in the Model Section. To access the API data, a framework called Spotipy was used. The reasons for this are the following:
- Makes the code more readable.
- It is straightforward to use and understand.
- Brings objects ready to use as python dictionaries and lists.

[PostgreSQL](https://www.postgresql.org) was chosen as well, given it is one the best relational databases, supported by the community and frequently used in Data Engineering projects. 

[Flask](https://flask.palletsprojects.com) framework was used given it is lightweight and works seamlessly with SQLAlchemy, a tool that was mandatory to this project. 

A REST API was built using [Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/
) to build JSON schemas, providing the DB objects fetched by SQLAlchemy.

## Bonuses
- [Running the application on a local environment](##Running-the-application-on-a-local-environment)
- [Docker](###Docker-Container)
- Data Transformation
- [Directory Structure](###Tree-Structure)
