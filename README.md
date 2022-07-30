# Data Engineering Starter Project
### Spotify Service
> Juan Sebastián Vargas C.
> Loka - Data Analyst Intern

# Introduction
Introduction
Python service which provides an API to simulate some Spotify features. It is a system that saves Spotify data on a relational database, and can be accessed through an API. It can be accessed both through the API or a connection on top of the Database.

The source of information is the Spotify web public API. The level of detail and data features are described below in the Model Section. To access the API data, a framework called Spotipy was used. The reasons for this are the following:
Makes the code more readable.
It is straightforward to use and understand.
Brings objects ready to use as python dictionaries and lists.
It has of course some caveats including the fact that it doesn’t get updated as soon as the official Spotify API releases any update. However, it was chosen given the advantages it offered to this project.

PostgreSQL was chosen as well, given it is one the best relational databases, supported by the community and frequently used in Data Engineering projects. 

Flask framework was used given it is lightweight and works seamlessly with SQLAlchemy, a tool that was mandatory to this project. A REST API was built using Marshmallow to build JSON schemas to provide the DB objects fetched by SQLAlchemy.



## Requirements
```python
# capture requirements to install
pip freeze > requirements.txt

# install requirements from requirements.txt
pip install -r requirements.txt
```

## Environment Variables - Flask
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