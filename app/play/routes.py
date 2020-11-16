from flask import (render_template, request,
    redirect, url_for, session)
from . import play
from .bridgit import Bridgit
from app import socketio

@play.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        session['level'] = request.form['diff-button']
        session['f_move'] = request.form['f-move']
        return redirect(url_for('play.play_game'))
    return render_template('index.html')

@play.route('/play')
def play_game():
    level = session.get('level', '')
    f_move = session.get('f_move', '')
    if level != '' and f_move != '':
        return render_template('play.html')
    else: return redirect(url_for('play.index'))

