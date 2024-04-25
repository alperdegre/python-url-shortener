from typing import Annotated
from fastapi import Header, HTTPException

async def get_user_id(authorization: Annotated[str, Header()]):
    if authorization is None or not validate_authorization(authorization):
        print("Invalid Auth")
        raise HTTPException(status_code=400, detail="Unauthorized")



def validate_authorization(auth_header:str):
    return True
    
