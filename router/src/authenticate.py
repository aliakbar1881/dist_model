import jwt
import hashlib
from datetime import datetime


class Authenticate:
    def __init__(self):
        self.secret_key = "dist_model_server"
        self.user_ids = [
            "123456789",
            "987654321",
            "098765432",
            "234567890",
        ]

    def authenticate(self, auth_data):
        """
        Authenticate client based on provided auth data.
        
        :param auth_data: Dictionary containing authentication details.
                        Expected format: {'token': 'jwt_token'}
        :return: True if authenticated successfully, False otherwise.
        """
        if not isinstance(auth_data, dict) or 'token' not in auth_data:
            return False
        try:
            payload = jwt.decode(auth_data['token'], self.secret_key, algorithms=['HS256'])
            if payload.get('user_id') in self.user_ids:
                return True
        except jwt.ExpiredSignatureError:
            print("Authentication token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid authentication token.")
        return False

    def get_user_id_from_auth(self, auth_data):
        """
        Extract user ID from authenticated data.
        
        :param auth_data: Dictionary containing authentication details.
                        Expected format after successful decode: {'user_id': '123'}
                        If using JWT, this is typically extracted from the decoded payload.
        
        :return: User ID string if found; otherwise None or raises an exception depending on requirements.
                In this example, we assume it's directly available in the decoded JWT payload or similar structure.
                Adjust according to how you handle user IDs during authentication flow (e.g., database lookup).
        
                Note: This function assumes a successful decode has already occurred,
                    so it doesn't handle decoding errors here but focuses on extracting the user ID from valid payloads.
                    You may want to add error handling based on your application's needs and architecture (e.g., database queries).
        """
        try:
            payload = jwt.decode(auth_data['token'], self.secret_key, algorithms=['HS256'])
            return payload.get('user_id')
        except Exception as e:
            print(f"Failed to extract user ID due to {str(e)}")


if __name__ == "__main__":
    auth = Authenticate()
    sample_payload = {'user_id': '234567890', 'exp': int(datetime.now().timestamp()) * 1000}
    sample_token = jwt.encode(sample_payload, auth.secret_key, algorithm='HS256')
    auth_example = {'token': sample_token}
    if auth.authenticate(auth_example):
        print(auth.get_user_id_from_auth(auth_example))
    else:
        print("Authentication failed.")
