import hashlib
import base64
import uuid
import random

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

def hash(s):
    return hashlib.md5(s.encode()).hexdigest()

def encode(s):
    return base64.b64encode(s.encode()).decode()
def decode(s):
    return base64.b64decode(s.encode()).decode()
def get_tok():
    return str(uuid.uuid1())
'''
def aget():
    private = rsa.generate_private_key(
                                    public_exponent = random.randint(65536, 2000000),
                                    key_size = 2048,
                                    backend=default_backend())
    return private.public_key(), private
def aencrypt(s, k):
    # base64 encode
    # encrypt
    return s
def adecrypt(s, k):
    # base64 decode
    return s

'''
