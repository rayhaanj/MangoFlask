from flask import Flask

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from flask_bootstrap import Bootstrap

engine = create_engine('')
db_session = Session(bind=engine)
Base = declarative_base()

def create_tables():
    from application import models
    Base.metadata.create_all(bind=engine)

app = Flask(__name__)
Bootstrap(app)

from application.public_views import *
from application.auth import *
from application.API import api_module

app.register_blueprint(api_module)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)