from flask import Flask
from flask_socketio import Socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SomeSecretKey'
socketio = Socketio(app)

if __name__ == '__main__':
    socketio.run(app)

