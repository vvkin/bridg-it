from flask import session, request
from flask_socketio import emit
from app import socketio, games
from app.play.bridgit import Bridgit

@socketio.on('connect', namespace='/play')
def on_connect():
    user_id = request.sid
    game = Bridgit(session['level'], session['f_move'])
    print(session['level'], session['f_move'])
    games[user_id] = game
    emit('draw field', {'moveNow': games[user_id].f_move})

@socketio.on('validate move', namespace='/play')
def validate_move(move):
    user_id = request.sid
    if games[user_id].is_valid(move):
        emit('valid move')

@socketio.on('player move', namespace='/play')
def player_move(move):
    pass

@socketio.on('disconnect', namespace='/play')
def on_disconnect():
    user_id = request.sid
    del games[user_id]
