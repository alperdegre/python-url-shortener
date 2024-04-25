import datetime
from Crypto.Hash import SHA256
import os 
import jwt
from pydantic import BaseModel, Field

class JWTRequest(BaseModel):
    username: str
    exp: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now() + datetime.timedelta(hours=24))

def create_url_hash(size:int):
    random_bytes = os.urandom(32)
    hash_object = SHA256.new(data=random_bytes)
    random_hash = hash_object.hexdigest()
    return random_hash[:size]


def create_jwt(data:JWTRequest):
    encoded = jwt.encode(data.model_dump(), "secret", algorithm="HS256")
    return encoded

def decode_jwt(jwtToken:str):
    decoded = ""
    try:
        decoded = jwt.decode(jwtToken, "secret", algorithms=["HS256"])
        return decoded, None
    except jwt.InvalidSignatureError:
        print("Invalid secret key")
        return None, "Invalid secret key"
    except jwt.DecodeError:
        print("Error decoding jwt")
        return None, "Error while decoding"
    except jwt.ExpiredSignatureError:
        print("JWT Expired")
        return None, "JWT has expired"
    except Exception as e:
        return None, "An unexpected error has occured"
