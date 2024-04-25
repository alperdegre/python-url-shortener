from Crypto.Hash import SHA256
import os 
import jwt
from pydantic import BaseModel

class JWTRequest(BaseModel):
    username: str

def create_url_hash(size:int):
    random_bytes = os.urandom(32)
    hash_object = SHA256.new(data=random_bytes)
    random_hash = hash_object.hexdigest()
    print(random_hash[:size])


def create_jwt(data:JWTRequest):
    encoded = jwt.encode(data.dict(), "secret", algorithm="HS256")
    return encoded

def decode_jwt(jwtToken:str):
    decoded = jwt.decode(jwtToken, "secret", algorithms=["HS256"])
    return decoded

