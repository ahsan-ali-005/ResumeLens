import bcrypt



def hash_password(password: str):

    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes,salt=salt).decode("utf-8")