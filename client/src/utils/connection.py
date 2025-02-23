import socketio
import json
from pathlib import Path
from src.utils.const import Constants
from src.utils.io import write



class SocketIOClient:
    def __init__(self, retriver):
        self.sio = socketio.Client()
        self.retriver = retriver
        self.const = Constants()
        self.auth_data = {'auth_data': self.const.token}

        # Register event handlers
        @self.sio.event
        def connect():
            print("Connected to the server")

        @self.sio.event
        def disconnect():
            print("Disconnected from the server")

    def on_query(self, data):
        query = data['query']
        target_client_id = data['target_client']
        response = self.retriver.retrieve(query, remote=False)
        self.send_response(target_client_id, response)

    def connect_to_server(self):
        print(self.const.server_url)
        self.sio.connect(self.const.server_url, auth=self.auth_data, transports=['websocket'])
        
    def send_query(self, query):
        self.sio.emit('query', {'auth_data': , 'query': query})

    def send_response(self, target_client_id, response):
        self.sio.emit('response', {'target_client_id': target_client_id, 'response': response})

    def on_response(self, data):
        response = data['response']
        self.write_to_temp(response)

    def write_to_temp(self, response):
        path = Path(self.cosnt.path) / "temp/response.json"
        write(path, json.dumps(response))

    def __call__(self):
        @self.sio.on('query')
        def receive_query(data):
            self.on_query(data)
        
        @self.sio.on('response')
        def receive_response(data):
            self.on_response(data)

        self.connect_to_server()
