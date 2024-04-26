from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from app.utils import JWTRequest, create_jwt
import bcrypt
from app.db.db import get_db
from app.db.repository import create_user, get_user_by_username
from ..models import AuthRequest, AuthResponse

router = APIRouter(
prefix="/auth",
)

testdb = []

@router.post("/signup")
async def signup(request: AuthRequest, db: Session = Depends(get_db)):
    body = request.model_dump()

    existing_user = get_user_by_username(body['username'], db)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error":"User already exists"})

    hashed = bcrypt.hashpw(body['password'].encode('utf-8'), bcrypt.gensalt())
    body['password'] = hashed
 
    user = create_user(AuthRequest(**body), db)

    jwt_request = JWTRequest(user_id=user['id'], username=user['username'])

    jwt = create_jwt(jwt_request)

    exp = jwt_request.model_dump()['exp']
    return AuthResponse(token=jwt, userID=user['id'], expiry=exp)


@router.post("/login")
async def login(request: AuthRequest, db: Session = Depends(get_db)):
    body = request.model_dump()

    existing_user = get_user_by_username(body['username'], db)

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error":"User does not exist"})

    user_dict = existing_user.model_dump()

    input_password_bytes = body['password'].encode('utf-8')
    stored_password_bytes = user_dict['password'].encode('utf-8')

    if bcrypt.checkpw(input_password_bytes,stored_password_bytes) == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error":"Incorrect username or password"})
    
    jwt_request = JWTRequest(user_id=user_dict['id'], username=user_dict['username'])

    jwt = create_jwt(jwt_request)
    
    exp = jwt_request.model_dump()['exp']

    return AuthResponse(token=jwt, userID=user_dict['id'], expiry=exp)

