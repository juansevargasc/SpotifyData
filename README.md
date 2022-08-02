# Data Engineering Starter Project
### Spotify Service
> Juan Sebastián Vargas C.
> Loka - Data Analyst Intern


## Running the application on a local environment

### Docker Container
[Docker](Dockerfile)

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

# Introduction
Introduction
Python service which provides an API to simulate some Spotify features. It is a system that saves Spotify data on a relational database, and can be accessed through an API. It can be accessed both through the API or a connection on top of the Database.

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
