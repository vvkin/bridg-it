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

    if not f_move: # now bot turn (first move)
        bot_move = game.get_move()
        data = {'x': bot_move[0], 'y': bot_move[1], 'color': color}
        emit('bot move', data)

@socketio.on('validate move', namespace='/play')
def on_validate_move(data):
    user_id = request.sid
    game = games[user_id]
    move = (data['x'], data['y'])

    if game.is_valid(move):
        game.set_move(move)
        emit('player move', game.f_move)

        if game.is_over(): 
            emit('game is over', {'winner': game.winner})
        else:
            bot_move = game.get_move()
            data = {'x': bot_move[0], 'y': bot_move[1], 'color': not game.f_move}
            emit('bot move', data)

            if game.is_over(): 
                emit('game is over', {'winner': game.winner})

@socketio.on('disconnec', namespace='/play')
def on_disconnect():
    user_id = request.sid
    del session['f_move']
    del session['level']
    del session['color']
    del games[user_id]
