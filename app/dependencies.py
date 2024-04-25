from typing import Annotated
from fastapi import Header, HTTPException

async def get_auth_token(authorization: Annotated[str, Header()]):
    print(authorization)
    if authorization == "":
        print("No authorization header set")
        raise HTTPException(status_code=400, detail="Unauthorized")
