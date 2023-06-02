from fastapi import APIRouter
from typing import List
from models.quiz import Quiz
import os
from mongo.mongo import client

router = APIRouter()

@router.get("/quiz", response_model=List[Quiz], status_code=200)
async def createQuiz():
    # Fetch the first document
    db_name = os.getenv("REACT_APP_DB_QUIZ")
    collection_name = os.getenv("REACT_APP_QUIZ_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    quiz = await collection.find().to_list(2)
    print(quiz)
    # Convert ObjectId to string and return the document
    return quiz