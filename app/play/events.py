from flask import session
from flask_socketio import emit
from app import socketio
from app.play.bridgit import Bridgit


@socketio.on('connect')
def connect():
    print('Connected')

@socketio.on('new game')
def new_game(level='low'):
    print('NEW GAME\n\n\n\n\n')
    session['game'] = Bridgit(level, 1)
    socketio.emit('draw field', broadcast=True)

@socketio.on('validate move')
def validate_move(move):
    game = session['game']
    if game.is_valid(move):
        emit('valid move')

@socketio.on('player move')
def player_move(move):
    game = session['game']
    bot_move = game.handle_move(move)
    emit('bot move', bot_move)

    if game.is_over():
        emit('end game', game.winner)