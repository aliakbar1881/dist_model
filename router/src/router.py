from flask import Flask, request
from flask_socketio import SocketIO, emit
from src.authenticate import Authenticate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dist_model_server'
socketio = SocketIO(app)

clients_connected = {}

auth = Authenticate()

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print("this is works")
    auth_data = request.args.get('auth_data')
    if auth.authenticate(auth_data):
        user_id = auth.get_user_id_from_auth(auth_data)
        if user_id not in clients_connected:
            clients_connected[user_id] = sid
        print(f"Client {user_id} connected")
        emit('connected', {'data': 'Connected successfully'})
    else:
        handle_disconnect()
        return False

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for user_id, stored_sid in list(clients_connected.items()):
        if stored_sid == sid:
            del clients_connected[user_id]
            print(f"Client {user_id} disconnected")

@socketio.on('query')
def handle_query(data):
    user_id = clients_connected[request.sid]
    for target_id, target_sid in clients_connected.items():
        emit('query', data['query'], room=target_sid)

@socketio.on('response')
def handle_response(data):
    target_client_id = data.get('target_client')
    if target_client_id in clients_connected:
        target_sid = clients_connected[target_client_id]
        emit('response', data['response'], room=target_sid)


if __name__ == '__main__':
    socketio.run(app)
