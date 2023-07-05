from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "b52c1fa330a2e6e53ee37ea164f1ae623dfaca7ace1bc8e1af6d69677bc048e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def token_response(token: str):
    """Function returns generated tokens (JWTs)"""
    return {
        "access token": token
    }

def signJWT(username: str):
    payload = {
        "username": username,
        "expiry"
    }