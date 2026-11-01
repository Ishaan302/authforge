# used argon2 which is a pswd hashing algo 
# argo2 uses random SALT when hashing same pswd  
# salt is a randomly generated string added to users pswd before hashing ,main purpose is to ensure that 2 users with same pswd get diff pswd hash   

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str: # this fxn accepts plaintext pswd and returns its hash
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:  # this fxn used during login,accepts 2 values and returns boolean
    return password_hasher.verify(password, hashed_password)



####  jwt part
# instead of repeatidly sends credentials ,authenticate the user once,after successful login server gives client a token,consist of  3 parts
# 1. header --  contains info about token type nd signing info
# 2. payload -- contains user identidy nd expiry 
# 3. signature -- Cryptographically verifies that the header and payload have not been modified.
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),  # identity of the user is user_id
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30) # token expires after 30 mint 
    }

    token = jwt.encode(  # creating the token
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(   # verify thr token
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload
    
    except jwt.InvalidTokenError:
        return None