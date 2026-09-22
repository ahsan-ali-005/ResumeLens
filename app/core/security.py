import bcrypt, jwt
from datetime import datetime, timezone, timedelta
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def hash_password(password: str):

    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes,salt=salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):

    pwd_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


def create_token(payload: dict):

    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp" : expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

