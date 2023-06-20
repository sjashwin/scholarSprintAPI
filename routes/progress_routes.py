from mongo.mongo import QUIZ_COLLECTION, QUESTION_COLLECTION, PROGRESS_COLLECTION
from mongo.PyObjectId import PyObjectId
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

class Progress(BaseModel):
    t: str
    d: str
    qID: str = ""
    quID: List[str] = []
    r: int = 0

class Progress(BaseModel):
    id: Optional[PyObjectId] = Field(default_factor=PyObjectId, alias='_id')
    uid: str
    score: int
    progress: List[Progress] = []
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

@router.get("/quizCount")
async def quizCount():
    count = await QUIZ_COLLECTION.count_documents({})
    return {"total": count}

@router.get("/questionCount")
async def questionCount():
    count = await QUESTION_COLLECTION.count_documents({})
    return {"total": count}

@router.get("/progress")
async def read_progress(userID: Optional[str] = None):
    if userID is None:
        doc = await PROGRESS_COLLECTION.find({}).to_list(None)
        for progress in doc:
            progress["_id"] = str(progress["_id"])
    else:
        doc = await PROGRESS_COLLECTION.find_one({"uid": userID})
        doc["_id"] = str(doc["_id"])
        quizAttempted = len(doc["progress"])
        score = 0
        for quiz in doc["progress"]:
            score = sum(1 for dictionary in quiz["quID"] if 1 in dictionary.values())
    return {"attempted": quizAttempted, "overall_score": score}