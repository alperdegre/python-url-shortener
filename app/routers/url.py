from fastapi import APIRouter, Depends

from app.db.repository import create_url
from sqlalchemy.orm import Session

from ..models import ShortenURLRequest
from app.utils import create_short_url, create_url_hash
from ..dependencies import get_user_id
from app.db.db import get_db

router = APIRouter(
prefix="/url",
dependencies=[Depends(get_user_id)]
)

@router.post("/shorten")
async def shorten(request: ShortenURLRequest,userId: int = Depends(get_user_id), db: Session = Depends(get_db)):
    hash = create_url_hash(10)
    short_url = create_short_url(hash)
    return create_url(request, short_url, db)

@router.get("/get")
async def get_urls(userId: int = Depends(get_user_id),db: Session = Depends(get_db)):
    print(userId)
    return {"message":"done"}

@router.delete("/delete/{url_id}")
async def delete_url(userId: int = Depends(get_user_id),db: Session = Depends(get_db)):
    return {"message":"done"}

