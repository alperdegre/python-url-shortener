import datetime 
from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    userID: int
    expiry: int

class ShortenURLRequest(BaseModel):
    url: str

class UserResponse(BaseModel):
    id: int
    username: str

class UserRecord(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime.datetime

class URLRecord(BaseModel):
    id: int
    created_at: datetime.datetime
    user_id: int
    short_url: str
    long_url: str

class JWTRequest(BaseModel):
    user_id: int
    username: str
    exp: int = Field(default_factory=lambda: int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)).timestamp()))

