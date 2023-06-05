from fastapi import APIRouter, Request, status, HTTPException
from typing import List
from models.quiz import Quiz
import os
from mongo.mongo import client

router = APIRouter()

@router.get("/createquiz", response_model=List[Quiz], status_code=200)
async def createQuiz(request: Request):
    db_name = os.getenv("REACT_APP_DB_QUIZ")
    collection_name = os.getenv("REACT_APP_QUIZ_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    quiz = await collection.find().to_list(2)

    return quiz