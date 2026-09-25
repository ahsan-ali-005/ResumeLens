import bcrypt, jwt
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.core.redis import redis_client
from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)

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


def verify_token(token: str) -> dict:
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has been blacklisted/revoked."
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(token) > 0


def blacklist_token(token,exp):

    current_time = datetime.now(timezone.utc).timestamp()
    ttl = int(exp - current_time)
    if ttl > 0:
        redis_client.set(token , "blacklisted", ex=ttl)


def create_verification_token(email: str):

    token = serializer.dumps(email, salt="email-verification")
    return token

def verify_verification_token(token: str , max_age : int = 86400):
    try:
        email = serializer.loads(token, max_age=max_age, salt="email-verification")
        return email

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")