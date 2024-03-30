from flask_app import app
from settings import SERVER_PORT
from socketio_event import socketio

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=SERVER_PORT, debug=True)
