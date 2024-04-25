from typing import Annotated
from fastapi import Header, HTTPException

from app.utils import decode_jwt

async def get_user_id(authorization: Annotated[str, Header()]):
    if authorization is None:
        print("Invalid Auth")
        raise HTTPException(status_code=400, detail="Unauthorized")

    user, error = validate_authorization(authorization)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return user
    
def validate_authorization(auth_header:str):
    decoded, error = decode_jwt(auth_header)

    if error:
        return None, error

    return decoded, None
    
