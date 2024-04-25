from fastapi import APIRouter, Depends
from ..dependencies import get_user_id

router = APIRouter(
prefix="/url",
dependencies=[Depends(get_user_id)]
)

@router.post("/shorten")
async def shorten():
    return [{"test1":"url1"}, {"test2":"url2"}]

@router.get("/get")
async def get_urls():
    return {"message":"done"}

@router.delete("/delete/{url_id}")
async def delete_url(url_id:str):
    return {"message":"done"}

