from fastapi import APIRouter, status
from mongo.mongo import ISSUE_COLLECTION 
import logging

router = APIRouter()

@router.post("/issues")
async def issues(data: dict):
    result = await ISSUE_COLLECTION.insert_one(data)
    logging.debug(f"{result.acknowledged}")
    return {"status": status.HTTP_200_OK, "result": result.acknowledged}
