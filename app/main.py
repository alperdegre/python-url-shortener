from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.db.db import Base, try_create
from app.utils import JWTRequest, create_jwt, decode_jwt
from .routers import auth, url

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
async def redirect_route(hash:str) -> RedirectResponse:
    return RedirectResponse(url="")

@app.get("/")
def test_route():
    encoded = create_jwt(JWTRequest(username="alperdegre", user_id="1"))
    decoded = decode_jwt(encoded)
    return {"Hello":"World", "encoded":encoded, "decoded":decoded}
