from mongo.mongo import QUIZ_COLLECTION, QUESTION_COLLECTION
from fastapi import APIRouter

router = APIRouter()

@router.get("/quizCount")
async def quizCount():
    count = await QUIZ_COLLECTION.count_documents({})
    return {"total": count}

@router.get("/questionCount")
async def questionCount():
    count = await QUESTION_COLLECTION.count_documents({})
    return {"total": count}