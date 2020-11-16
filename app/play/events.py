from flask import session, request
from flask_socketio import emit, send, disconnect
from app import socketio, games
from app.play.bridgit import Bridgit

@socketio.on('connect', namespace='/play')
def on_connect():
    user_id = request.sid
    game = Bridgit(session['level'], session['f_move'])
    games[user_id] = game
    emit('draw field', {'moveNow': games[user_id].f_move})

    if not session['f_move']: # now bot turn
        bot_move = game.get_move()
        emit('bot move', {'x': bot_move[0], 'y': bot_move[1]})

@socketio.on('validate move', namespace='/play')
def on_validate_move(data):
    user_id = request.sid
    game = games[user_id]
    move = (data['x'], data['y'])

    if game.is_valid(move):
        game.set_move(move)
        emit('player move', {'x': move[0], 'y': move[1]}, )

        if game.is_over():
            emit('game over', {'winner': game.winner})
        else:
            bot_move = game.get_move()
            emit('bot move', {'x': bot_move[0], 'y': bot_move[1]})

@socketio.on('disconnect', namespace='/play')
def on_disconnect():
    print("\n\n\nDISCONNECT!\n\n\n")
    user_id = request.sid
    del session['f_move']
    del session['level']
    del games[user_id]
        

