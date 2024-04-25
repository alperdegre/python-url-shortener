from datetime import datetime
from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

class ShortenURLRequest(BaseModel):
    long_url: str
    user_id: int

class UserRecord(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime

class URLRecord(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    short_url: str
    long_url: str
