__author__ = 'rayhaan'

from flask import render_template, Response
from application import app, db, models

@app.route('/')
def home():
    blog_posts = models.BlogPost.query.filter_by(draft=False).limit(5)
    return render_template('index.html', blog_posts=blog_posts, active='home')

@app.route('/blog')
def blog():
    blog_posts = models.BlogPost.query.filter_by(draft=False).limit(10)
    return render_template('blog.html', blog_posts=blog_posts, active='blog')

@app.route('/blog/<int:id>')
def view_blogpost(id):
    post = models.BlogPost.query.filter_by(id=id).first()
    if post is None:
        return Response('<h1>Post not found!</h1>', status=404)
    return render_template('blog_post.html', post=post, active='blog')

@app.route('/contact')
def contact():
    return render_template('contact.html', active='contact')