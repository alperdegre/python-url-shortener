from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from app.db.db import Url, User
from app.models import UserResponse
from ..models import AuthRequest, URLRecord, UserRecord, ShortenURLRequest
from sqlalchemy.orm import Session

# Get User - Create User - Create Url - Get Url from Short - Get Url from Long
# Get user Urls, delete url

def get_user_by_id(user_id:int, db:Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    return UserRecord(**db_user.__dict__)

def get_user_by_username(username:str, db:Session):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        return None
    return UserRecord(**db_user.__dict__)

def create_user(auth_request:AuthRequest, db: Session):
    db_user = User(**auth_request.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_dict = db_user.__dict__
    del db_dict['password']
    del db_dict['created_at']
    return db_dict 
        
def create_url(url_request:ShortenURLRequest, short_url:str, user_id:int, db:Session):
    dumped_req = url_request.model_dump()
    db_url = Url(short_url=short_url, long_url=dumped_req['url'], user_id=user_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return URLRecord(**db_url.__dict__)

def get_url_from_short_url(short_url:str, db:Session):
    db_url = db.query(Url).filter(Url.short_url == short_url).first()
    if db_url is None:
        return None
    return URLRecord(**db_url.__dict__)

def get_url_from_long_url(long_url:str, db:Session):
    db_url = db.query(Url).filter(Url.long_url == long_url).first()
    if db_url is None:
        return None
    return URLRecord(**db_url.__dict__)

def get_url_from_id(url_id:int, db:Session):
    db_url = db.query(Url).filter(Url.id == url_id).first()
    if db_url is None:
        raise NoResultFound()
    return db_url

def get_user_urls(user_id:int, db:Session):
    user_urls = db.query(Url).filter(Url.user_id == user_id).all()
    return [url.__dict__ for url in user_urls]

def delete_url_from_db(url_id:int, db:Session):
    db_url = get_url_from_id(url_id, db)
    db.delete(db_url)
    db.commit()

    return URLRecord(**db_url.__dict__)
