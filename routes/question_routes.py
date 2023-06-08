from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel
from models.question import Question
from mongo.mongo import client
import os

class QuestionParam(BaseModel):
    size: Optional[int] = None
    subDomain: Optional[int] = None
    domain: Optional[int] = None


router = APIRouter()

@router.post("/questions", response_model=List[Question], status_code=200)
async def createRoom(params: QuestionParam=None):
    db_name = os.getenv("REACT_APP_DB")
    collection_name = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    questions = await collection.find().to_list(2)
    return questions