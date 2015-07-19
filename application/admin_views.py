__author__ = 'rayhaan'

from flask import Blueprint, render_template
from application.auth import logged_in

admin_module = Blueprint('admin', __name__)

@admin_module.route('/')
@logged_in
def home():
    return render_template('dashboard.html')
