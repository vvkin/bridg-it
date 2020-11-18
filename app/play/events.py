from flask import session, request
from flask_socketio import emit, send, disconnect
from app import socketio, games
from app.play.bridgit import Bridgit

@socketio.on('connect', namespace='/play')
def on_connect():
    user_id = request.sid
    level = session['level']
    f_move = int(session['f_move'])
    color = int(session['color'])
    game = Bridgit(level, f_move, color)
    games[user_id] = game
    emit('draw field', {'moveNow': f_move})

@socketio.on('validate move', namespace='/play')
def on_validate_move(data):
    user_id = request.sid
    game = games[user_id]
    move = (data['x'], data['y'])

    if game.is_valid(move):
        game.set_move(move)
        data = {'x': move[0], 'y': move[1], 'color': game.color_idx}
        emit('player move', data)

@socketio.on('is over', namespace='/play')
def on_is_over():
    user_id = request.sid
    game = games[user_id]

    if game.is_over(): # player won
        emit('game is over', game.winner)
    else:
        bot_move = game.get_move()
        data = {'x': bot_move[0], 'y': bot_move[1], 'color': not game.color_idx}
        emit('bot move', data)

        if game.is_over(bot_move): # bot won
            emit('game is over', game.winner)

@socketio.on('disconnect', namespace='/play')
def on_disconnect():
    user_id = request.sid
    del session['f_move']
    del session['level']
    del session['color']
    del games[user_id]
