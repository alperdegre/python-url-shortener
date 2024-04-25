from fastapi import APIRouter

router = APIRouter()

@router.get("/url")
async def url_test():
    return [{"test1":"url1"}, {"test2":"url2"}]
