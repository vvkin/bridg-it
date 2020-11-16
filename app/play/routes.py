from flask import (render_template, request,
    redirect, url_for, g)
from . import play
from .bridgit import Bridgit

@play.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        level = request.form['diff-button']
        f_move = request.form['f-move']
        g.game = Bridgit(level, f_move)
        return redirect(url_for('play.play_game'))
    
    return render_template('index.html')

@play.route('/play')
def play_game():
    return render_template('play.html')
