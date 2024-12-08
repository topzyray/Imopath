from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging


# Handling password hashing
password_context = CryptContext(
    schemes=['bcrypt']
)


# Amount of time in seconds
ACCESS_TOKEN_EXPIRY = 3600


# Generate new password hash
def generate_password_hash(password: str) -> str:
    hash = password_context.hash(password)

    return hash


# Verifies the password hash
def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


# Generate new access token
def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4)

    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


# Decode access token
def decode_token(token: str) -> dict:

    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=Config.JWT_ALGORITHM
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


