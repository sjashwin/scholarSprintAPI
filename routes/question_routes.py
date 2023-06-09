from fastapi import APIRouter, Request, HTTPException, status
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
async def questions(request: Request, params: QuestionParam=None):
    db_name = os.getenv("REACT_APP_DB")
    collection_name = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    questions = await collection.find(params).to_list(2)

    for question in questions:
        question["_id"] = str(question["_id"])
        # Get username from the session
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")

    # Map the quiz to the username and add it to the session
    request.session[username] = [q for q in questions]
    print("Questions:", request.session[username])
    return questions

@router.post("/validate/{index}/{answer}")
async def validate(index: int, answer: str, request: Request):
    # Get username from the session
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")

    # Get the list of questions from the session
    questions = request.session[username]
    if not questions or index >= len(questions):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid question index")

    # Retrieve the question from the session
    question = questions[index]
    if question["a"][0] == answer:
        return {"message": "Correct Answer"}
    else:
        return {"message": "Incorrect Answer"}
    # Validate the answer