from hashlib import sha256
from os import environ

def hash_string(phrase):
    to_encrypt = phrase + environ.get("SECRET_SALT")
    return sha256(to_encrypt.encode()).hexdigest()
