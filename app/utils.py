from Crypto.Hash import SHA256
import os 
from fastapi import HTTPException
import jwt
import math

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.db.repository import get_url_from_short_url
from .models import JWTRequest
from sqlalchemy.orm import Session

def create_url_hash(size:int, db:Session):
    hash=None

    for i in range(30):
        hash_try = create_and_check_hash(size, i, db)
        if hash_try is not None:
            hash = hash_try
            break

    return hash

def create_and_check_hash(size:int,i:int, db:Session):
    random_bytes = os.urandom(32)
    hash_object = SHA256.new(data=random_bytes)
    random_hash = hash_object.hexdigest()
    shortened_hash = random_hash[:size+int(math.floor(i/10))]

    check_hash = get_url_from_short_url(shortened_hash, db)

    if check_hash is None:
        return shortened_hash
    else:
        return None


def create_short_url(hash:str):
    BASE_URL = os.getenv("BASE_URL")

    if BASE_URL is None:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail={"error":"Server error"})

    return BASE_URL + "/" + hash

def create_jwt(data:JWTRequest):
    encoded = jwt.encode(data.model_dump(), os.getenv("JWT_SECRET", ""), algorithm="HS256")
    return encoded

def decode_jwt(jwtToken:str):
    try:
        decoded = jwt.decode(jwtToken, os.getenv("JWT_SECRET", ""), algorithms=["HS256"])
        return decoded['user_id'], None
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
        print(f"An unexpected error occurred: {str(e)}")
        return None, "An unexpected error has occured"

