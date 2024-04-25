from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from app.db.db import Url, User
from app.models import UserResponse
from ..models import AuthRequest, URLRecord, UserRecord, ShortenURLRequest
from sqlalchemy.orm import Session

# Get User - Create User - Create Url - Get Url from Short - Get Url from Long
# Get user Urls, delete url

def get_user_by_id(user_id:int, db:Session) -> UserRecord :
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise NoResultFound()
    return UserRecord(**db_user.__dict__)

def get_user_by_username(username:str, db:Session) -> UserRecord :
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        return None
    return UserRecord(**db_user.__dict__)

def create_user(auth_request:AuthRequest, db: Session) -> UserRecord :
    db_user = User(**auth_request.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_dict = db_user.__dict__
    del db_dict['password']
    del db_dict['created_at']
    return db_dict 
        
def create_url(url_request:ShortenURLRequest, short_url:str, db:Session) -> URLRecord :
    dumped_req = url_request.model_dump()
    dumped_req["short_url"] = short_url
    db_url = Url(**dumped_req)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return URLRecord(**db_url.__dict__)

def get_url_from_short_url(short_url:str, db:Session) -> URLRecord:
    db_url = db.query(Url).filter(Url.short_url == short_url).first()
    if db_url is None:
        raise NoResultFound()
    return URLRecord(**db_url.__dict__)

def get_url_from_long_url(long_url:str, db:Session) -> URLRecord:
    db_url = db.query(Url).filter(Url.long_url == long_url).first()
    if db_url is None:
        raise NoResultFound()
    return URLRecord(**db_url.__dict__)

def get_url_from_id(url_id:int, db:Session) -> URLRecord:
    db_url = db.query(Url).filter(Url.id == url_id).first()
    if db_url is None:
        raise NoResultFound()
    return db_url

def get_user_urls(user_id:int, db:Session):
    user_urls = db.query(Url).filter(Url.user_id == user_id).all()
    return user_urls.__dict__

def delete_url(url_id:int, db:Session) -> URLRecord:
    db_url = get_url_from_id(url_id, db)
    db.delete(db_url)
    db.commit()

    return URLRecord(**db_url.__dict__)
