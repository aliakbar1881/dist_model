from dotenv import dotenv_values, load_dotenv
import jwt
from datetime import datetime


class Constants:
    def __init__(self):
        load_dotenv()
        envs = dotenv_values('.env')
        self.openai_key = envs['OPENAI_API_KEY']
        self.path = envs['PYTHONPATH']
        self.user_id = envs['USER_ID']
        self.server_url = envs['SERVER_URL']
        self.secret_key = envs['SECRET_KEY']

        payload = {'user_id': self.user_id, 'exp': int(datetime.now().timestamp()) * 1000}
        self.token = jwt.encode(payload, self.secret_key, algorithm='HS256')
