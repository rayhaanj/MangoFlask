__author__ = 'rayhaan'

from datetime import datetime

from flask import Blueprint, jsonify, Response, request, session

from application import models, db
from application.auth import logged_in

API_VERSION = 0.1

api_module = Blueprint('api', __name__)

@api_module.route('/', methods=['GET'])
def home():
    return jsonify(dict(version=API_VERSION, message='Welcome to the rayhaan.net API.'
                                                     + 'For a listing of endpoints go to /map'))
# Retrieve a listing of blog posts.
@api_module.route('/blog', methods=['GET'])
def blog_home():
    blog_posts = models.BlogPost.query.all()
    return jsonify(dict(data=blog_posts))

# Retrieve a particular blog post
@api_module.route('/blog/<int:id>', methods=['GET'])
def get_blog_post(id):
    blog_post = models.BlogPost.query.filter_by(id=id).first()
    if blog_post is None:
        return Response(jsonify(dict(error='Blog post not found!')), 404)
    return jsonify(dict(data=blog_post))

# Create a new blog post
@api_module.route('/blog', methods=['POST'])
@logged_in
def new_blogpost():
    title = request.form['title']
    draft = False if request.form['draft'] == 0 else True

    author_id = session.get('user_id', None)

    date_published = datetime.now()
    content = request.form['content']

    blog_post = models.BlogPost(title, author_id, draft, date_published=date_published,
                                content=content)

    db.session.add(blog_post)
    db.session.commit()

# Update an existing blog post
@api_module.route('/blog/<int:id>', methods=['PUT'])
def update_blogpost(id):
    post = models.BlogPost.query.filter_by(id=id).first()
    print("Start")
    if post is None:
        return Response(jsonify(dict(error='Blog post not found!')), 404)

    title = request.json['title']
    draft = request.json['draft']
    date_published = datetime.now()
    content = request.json['content']
    post.title = title
    post.draft = draft
    post.date_published = date_published
    post.content = content

    db.session.commit()
    return jsonify(dict(data=post))

@api_module.route('/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    post = models.BlogPost.query.filter_by(id=id).first()
    if post is None:
        return Response(jsonify(dict(error='Blog post not found!')), 404)
    post.deleted = True
    db.session.commit()
    return jsonify(dict(post=post))