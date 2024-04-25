from typing import Union

from fastapi import FastAPI

from app.utils import JWTRequest, create_jwt, create_url_hash, decode_jwt
from .routers import auth, url

app = FastAPI()

app.include_router(auth.router)
app.include_router(url.router)

@app.get("/")
def test_route():
    encoded = create_jwt(JWTRequest(username="alperdegre"))
    print(encoded)
    decoded = decode_jwt(encoded)
    print(decoded)
    return {"Hello":"World", "encoded":encoded, "decoded":decoded}
