from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from app.db.repository import create_url, delete_url_from_db, get_url_from_long_url, get_user_urls

from sqlalchemy.orm import Session
from ..models import ShortenURLRequest
from app.utils import create_short_url, create_url_hash
from ..dependencies import get_user_id
from app.db.db import get_db

router = APIRouter(
prefix="/api",
)

@router.post("/shorten")
async def shorten(request: ShortenURLRequest,userId: int = Depends(get_user_id), db: Session = Depends(get_db)):
    dict_url = request.model_dump()
    db_url = get_url_from_long_url(dict_url['url'], db)

    if db_url is not None:
        return db_url

    hash = create_url_hash(10, db)

    if hash is None:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error creating hash")

    return create_url(request, hash, db)

@router.get("/get")
async def get_urls(user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    urls = get_user_urls(user_id, db)
    return {"urls":urls}

@router.delete("/delete/{url_id}")
async def delete_url(url_id: str, userId: int = Depends(get_user_id),db: Session = Depends(get_db)):
    if userId == None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    deleted = delete_url_from_db(url_id, db)
    return {"url":deleted}

