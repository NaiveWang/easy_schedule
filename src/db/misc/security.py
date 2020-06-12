import hashlib
import base64
import uuid
import random

from cryptography.fernet import Fernet

def hash(s):
    return hashlib.md5(s.encode()).hexdigest()
def hash1(s):
    return hashlib.sha256(s.encode()).hexdigest()

def sencrypt(s, k):
    f = Fernet(hash1(k))
    # encrypt
    return f.encrypt(s.encode()).decode()
def sdecrypt(s, k):
    key = hash1(k)
    return f.decrypt(s.encode()).decode()

def encode(s):# bytes or string
    try:
        s = s.encode()
    except (UnicodeDecodeError, AttributeError):
        pass
    return base64.b64encode(s).decode()
def decode(s): # string
    return base64.b64decode(s.encode()).decode()
def get_tok():
    return str(uuid.uuid1())
