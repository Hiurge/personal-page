import os 
import datetime

class Config:

    SECRET_KEY = os.urandom(16)

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=10)
