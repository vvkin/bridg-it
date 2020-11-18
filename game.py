#!/bin/env python
from app import create_app, socketio

app = create_app(debug=False)

if __name__ == '__main__':
    socketio.run(app)