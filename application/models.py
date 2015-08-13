__author__ = 'rayhaan'

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask.json import JSONEncoder

from application import app, db

class SqlJsonEncoder(JSONEncoder):
    """Converts a SQLAlchemy mapped type to a json serializable dict."""
    def default(self, obj):
        try:
            if isinstance(obj, db.Model):  # Is another db object
                visited = []
                if obj in visited:
                    return None
                visited.append(obj)

                result = {}
                if '__json_fields__' in dir(obj):
                    fields = obj.__getattribute__('__json_fields__')
                else:
                    # TODO: After changing to flask-sqlalchemy this has changed and is broken.
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

class User(db.Model):
    __tablename__ = 'user'
    __json_fields__ = ['username', 'display_name']
    id = db.Column(db.Integer, primary_key=True, index=True)

    username = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(256))
    email_address = db.Column(db.String(256))

    display_name = db.Column(db.String(128), unique=True)

    # blog_posts backref from BlogPost.

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, attempt):
        return check_password_hash(self.password, attempt)

class BlogPost(db.Model):
    '''A blog post to display on the website.'''
    __tablename__ = 'blog_post'
    __json_fields__ = ['id', 'title', 'draft', 'deleted', 'author_id', 'date_published', 'content',
                       'author']

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(1024))

    draft = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='blog_posts')

    date_created = db.Column(db.DateTime)
    latest_revision_date = db.Column(db.DateTime)
    # The datetime to display publicly.
    date_published = db.Column(db.DateTime)

    content = db.Column(db.Text)

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

class EmoTrack(db.model):
    """Table for storing historical log of emotions"""
    __tablename__ = 'emotion_tracker'

    id = db.Column(db.Integer, primary_key=True)
    happinessrank = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    comment = db.column(db.String(128))

    def __repr__(self):
        return '<EmoTrack happiness=' + self.happinessrank + ', timestamp=' + self.timestamp +\
            ', comment=' + self.comment + '>'

    def __init__(self, happinessRank, timestamp=datetime.now(), comment=None):
        self.happinessrank = happinessRank
        self.timestamp = timestamp
        self.comment = comment
