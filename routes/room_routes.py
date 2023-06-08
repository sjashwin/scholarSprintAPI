from fastapi import APIRouter
from typing import List
import os
from models.question import Question
from mongo.mongo import client

router = APIRouter()
questions: List[Question] = []

@router.post("/create-room", response_model=List[Question], status_code=200)
async def createRoom():
    global questions
    db_name = os.getenv("REACT_APP_DB")
    collection_name = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    questions = await collection.find().to_list(2)
    return questions

@router.post("/validate")
async def validate_answer(data: dict):
    global questions
    questions[data["index"]].a = data["answer"]
    
