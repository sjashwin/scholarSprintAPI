from mongo.mongo import QUIZ_COLLECTION, QUESTION_COLLECTION, PROGRESS_COLLECTION
from mongo.PyObjectId import PyObjectId
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

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
            for obj in progress["progress"]:
                try:
                    progress["score"] += obj["r"]
                except:
                    pass
        return doc
    else:
        doc = await PROGRESS_COLLECTION.find_one({"uid": userID})
        doc["_id"] = str(doc["_id"])
        quizAttempted = set([quiz['qID'] for quiz in doc["progress"] if 'qID' in quiz])
        score = 0
        questionsAttempted = []
        for quiz in doc["progress"]:
            try:
                score = score + sum(value for dictionary in quiz["quID"] for value in dictionary.values())
                questionsAttempted.append(len(set(key for dictionary in quiz["quID"] for key in dictionary.keys())))
            except KeyError as e:
                logging(f"{e}")
    return {"attempted": len(quizAttempted), "score": score, "questionAttempted": sum(questionsAttempted)}