from flask import render_template
from . import play

@play.route('/')
def home_page():
    print('route')
    return render_template('index.html')