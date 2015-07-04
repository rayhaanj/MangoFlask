__author__ = 'rayhaan'

from flask import Blueprint, jsonify, Response, request

from application import db_session
from application import models

API_VERSION = 0.1

api_module = Blueprint('api', __name__)

@api_module.route('/', methods=['GET'])
def home():
    return jsonify(dict(version=API_VERSION, message='Welcome to the rayhaan.net API.'
                                                     + 'For a listing of endpoints go to /map'))
# Retrieve a listing of blog posts.
@api_module.route('/blog', methods=['GET'])
def blog_home():
    blog_posts = db_session.query(models.BlogPost).all()
    return jsonify(dict(blog_posts=blog_posts))

# Retrieve a particular blog post
@api_module.route('/blog/<int:id>', methods=['GET'])
def get_blog_post(id):
    blog_post = db_session.query(models.BlogPost).filter_by(id=id).first()
    if blog_post is None:
        return Response(jsonify(dict(error='Blog post not found!')), 404)
    return jsonify(dict(blog_post=blog_post))

# TODO(rayhaan) restricted
# Create a new blog post
@api_module.route('/blog', methods=['POST'])
def new_blogpost():
    title = request.form['title']
    draft = False if request.form['draft'] == 0 else True

    # TODO(rayhaan) When sessions are implemented insert id here.
    author_id = None

    date_published = request.form['date_published']
    content = request.form['content']

    blog_post = models.BlogPost(title, author_id, draft, date_published=date_published, content=content)

    db_session.add(blog_post)
    db_session.commit()

# TODO(rayhaan) restricted
# Update an existing blog post
@api_module.route('/blog/<int:id>', methods=['PUT'])
def update_blogpost(id):
    post = db_session.query(models.BlogPost).filter_by(id=id).first()
    if post is None:
        return Response(jsonify(dict(error='Blog post not found!')), 404)

    title = request.form['title']
    draft = False if request.form['draft'] == 0 else True

    date_published = request.form['date_published']
    content = request.form['content']

    post.title = title
    post.draft = draft
    post.date_published = date_published
    post.content = content

    db_session.commit()
    return jsonify(post)

@api_module.route('/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    post = db_session.query(models.BlogPost).filter_by(id=id).first()
    if post is None:
       return Response(jsonify(dict(error='Blog post not found!')), 404)
    post.deleted = True
    db_session.commit()
    return jsonify(post)