from flask import Flask, session
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'SomeSecretKey'

    from .play import play
    app.register_blueprint(play)
    socketio.init_app(app)
    return app
