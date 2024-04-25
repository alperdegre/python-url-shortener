import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.db.db import Base, try_create
from app.db.repository import get_url_from_short_url
from sqlalchemy.orm import Session
from .routers import auth, url
from app.db.db import get_db

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4000",
]

app.add_middleware(
   CORSMiddleware, 
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"], 
   allow_headers=["*"],)

app.include_router(auth.router)
app.include_router(url.router)

@app.on_event("startup")
async def startup():
    try_create()


@app.get("/{hash}")
async def redirect_route(hash:str, db: Session = Depends(get_db)) -> RedirectResponse:
    url_record = get_url_from_short_url(hash, db)

    if url_record == None:
        return RedirectResponse(os.getenv("BASE_URL", ""))
    
    url_dict = url_record.model_dump()
    return RedirectResponse(url=url_dict['long_url'])
