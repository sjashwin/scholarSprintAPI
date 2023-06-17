from fastapi import APIRouter, status, Request
from mongo.mongo import client
import os

router = APIRouter()

@router.post("/issues")
async def issues(data: dict):
    db_name=os.getenv("REACT_APP_DB_QUIZ")
    collection_name=os.getenv("REACT_APP_ISSUES_COLLECTIONS")
    db=client[db_name]
    collection=db[collection_name]
    result = await collection.insert_one(data)
    return {"status": status.HTTP_200_OK, "result": result.acknowledged}
