from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db.repository import create_user
# from ..dependencies import get_user_id
from ..models import AuthRequest

router = APIRouter(
prefix="/auth",
)

testdb = []

@router.post("/signup")
async def signup(request: AuthRequest, db: Session = Depends(get_db)):
    return create_user(request, db)

@router.post("/login")
async def login(request: AuthRequest):
    return [{"test1":"resp1"}, {"test2":testdb}]

