__author__ = 'rayhaan'

from datetime import datetime

from sqlalchemy import Boolean, Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask.json import JSONEncoder

from application import app, Base

class SqlJsonEncoder(JSONEncoder):
    """Converts a SQLAlchemy mapped type to a json serialisable dict."""
    def default(self, obj):
        try:
            if isinstance(obj, Base):  # Is another db object
                visited = []
                if obj in visited:
                    return None
                visited.append(obj)

                result = {}
                if '__json_fields__' in dir(obj):
                    fields = obj.__getattribute__('__json_fields__')
                else:
                    fields = [x for x in dir(obj) if not x.startswith('_')
                              and x != 'metadata']
                for field in fields:
                    result[field] = obj.__getattribute__(field)
                return result
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

# Set the JSON encoder to the one defined above.
app.json_encoder = SqlJsonEncoder

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(128), unique=True, index=True)
    password = Column(String(256))
    email_address = Column(String(256))

    display_name = Column(String(128), unique=True)

    # blog_posts backref from BlogPost.

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, attempt):
        return check_password_hash(self.password, attempt)

class BlogPost(Base):
    '''A blog post to display on the website.'''
    __tablename__ = 'blog_post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1024))

    draft = Column(Boolean)
    deleted = Column(Boolean)

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref='blog_posts')

    date_created = Column(DateTime)
    latest_revision_date = Column(DateTime)
    # The datetime to display publicly.
    date_published = Column(DateTime)

    content = Column(Text)

    def __repr__(self):
        return '<BlogPost title=' + str(self.title) + ', author_id = ' + str(self.author_id) + '>'

    def __init__(self, title, author_id, draft=True, date_created=datetime.now(), latest_revision_date=datetime.now(),
                 date_published=datetime.now(), content=None):
        self.title = title
        self.author_id = author_id
        self.draft = draft
        self.deleted = False
        self.date_created = date_created
        self.latest_revision_date = latest_revision_date
        self.date_published = date_published
        self.content = content
