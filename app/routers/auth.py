from fastapi import APIRouter, Depends
from fastapi.exceptions import BaseModel
from ..dependencies import get_auth_token

router = APIRouter(
prefix="/auth",
    # dependencies=[Depends(get_auth_token)]
)

class AuthRequest(BaseModel):
    username: str
    password: str

testdb = []

@router.get("/signup")
async def signup(request: AuthRequest):
    print(request)
    testdb.append(request)
    return [{"test1":"resp1"}, {"test2":"resp2"}]

@router.get("/signin")
async def signin(request: AuthRequest):
    return [{"test1":"resp1"}, {"test2":"resp2"}]

@router.get("/login")
async def login(request: AuthRequest):

    return [{"test1":"resp1"}, {"test2":testdb}]

