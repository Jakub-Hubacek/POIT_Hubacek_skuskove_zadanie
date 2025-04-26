from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from . import schemas
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # default is 15 minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception: Exception):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        personal_number: str = payload.get("sub")
        if personal_number is None:
            raise credentials_exception
        token_data = schemas.TokenData(personal_number=personal_number)
        return personal_number
    except JWTError:
        raise credentials_exception


def create_refresh_token(data: dict):
    to_encode = data.copy()
    # Set a longer lifespan for refresh token, e.g., 7 days
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str, credentials_exception: Exception):
    return verify_token(token, credentials_exception)
