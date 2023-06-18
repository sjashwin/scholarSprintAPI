from fastapi import APIRouter, status
from mongo.mongo import ISSUE_COLLECTION 

router = APIRouter()

@router.post("/issues")
async def issues(data: dict):
    result = await ISSUE_COLLECTION.insert_one(data)
    return {"status": status.HTTP_200_OK, "result": result.acknowledged}
