from flask import Flask
from flask import Markup
import markdown

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from flask_bootstrap import Bootstrap

import random
import string


app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(32))
Bootstrap(app)

app.config.from_object('application.config')

# Set default pool recycle time or configured value.
pool_recycle = app.config['DB_RECYCLE'] if 'DB_RECYCLE' in app.config else 3600

engine = create_engine(app.config['DB_URL'], pool_recycle=pool_recycle)
db_session = Session(bind=engine)
Base = declarative_base()

def create_tables():
    from application import models
    Base.metadata.create_all(bind=engine)

from application.public_views import *
from application.auth import *
from application.API import api_module
from application.admin_views import admin_module

app.register_blueprint(api_module, url_prefix='/api')
app.register_blueprint(admin_module, url_prefix='/admin')

def markdownify(text):
    return Markup(markdown.markdown(text))

def get_GAID():
    return app.config['GAID']

app.jinja_env.globals.update(markdownify=markdownify)
app.jinja_env.globals.update(get_GAID=get_GAID)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
