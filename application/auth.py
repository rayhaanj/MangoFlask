__author__ = 'rayhaan'

from flask import session, jsonify, Response, request, redirect, render_template, url_for
from functools import wraps
from application import app,db_session
from application import models

def logged_in(func):
    ''' Checks if a user is logged in before being allowed to run a particular function.
    :param func: The function to do the auth check before running.
    :return: A new function which checks if the user is logged in before proceeding.
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is not None:
            # User is logged in
            return func(*args, **kwargs)
        return Response(jsonify(dict(error='You are not logged in!')), 403, mimetype="application/json")
    return decorated_function

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = db_session.query(models.User).filter_by(username=username).first()
    if user is None:
        return redirect(url_for('login_get', error=True))
    if user.check_password(password):
        # User has successfully authenticated.
        session['logged_in'] = 1
        session['username'] = username
        session['user_id'] = user.id
        return redirect(url_for('admin.home'))
    return redirect(url_for('login_get', error=True))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))