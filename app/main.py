import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from app.db.db import Base, try_create
from app.db.repository import get_url_from_short_url
from sqlalchemy.orm import Session
from .routers import auth, url
from app.db.db import get_db

app = FastAPI()

origins = [
    "https://short.alperdegre.com",
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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.get("/{hash}")
async def redirect_route(hash:str, db: Session = Depends(get_db)) -> RedirectResponse:
    url_record = get_url_from_short_url(hash, db)

    if url_record == None:
        return RedirectResponse(url="https://short.alperdegre.com")
    
    url_dict = url_record.model_dump()
    return RedirectResponse(url=url_dict['long_url'])
