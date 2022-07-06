# Data Engineering Starter Project
### Spotify Service
> Juan Sebastián Vargas C.
> Loka - Data Analyst Intern

# Introduction
Python service which provides an API to simulate some Spotify features. 


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