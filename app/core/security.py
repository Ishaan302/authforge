# used argon2 which is a pswd hashing algo 
# argo2 uses random SALT when hashing same pswd  
# salt is a randomly generated string added to users pswd before hashing ,main purpose is to ensure that 2 users with same pswd get diff pswd hash   

from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str: # this fxn accepts plaintext pswd and returns its hash
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:  # this fxn used during login,accepts 2 values and returns boolean
    return password_hasher.verify(password, hashed_password)

