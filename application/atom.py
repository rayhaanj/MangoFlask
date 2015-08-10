from werkzeug.contrib.atom import AtomFeed

from application import app
from application import models
import markdown

from flask import request
__author__ = 'rayhaan'

@app.route('/blog.atom')
def blog_atom_feed():
    feed = AtomFeed('Recent Blog Posts', feed_url=request.url, url=request.url_root)
    posts = models.BlogPost.query.limit(15).all()
    for post in posts:
        feed.add(post.title, markdown.markdown(post.content),
                 content_type="html", author=post.author.display_name,
                 url="https://rayhaan.net/blog/" + str(post.id), updated=post.date_published)
    return feed.get_response()
