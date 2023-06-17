from fastapi import APIRouter, Request, HTTPException, status
from typing import List, Optional
from models.question import Question
from mongo.mongo import client
from bson import ObjectId
import os
import spacy
import random


router = APIRouter()

nlp = spacy.load("en_core_web_sm")

@router.post("/questions", response_model=List[Question], status_code=200)
async def questions(request: Request, quiz: Optional[dict] = {}):
    """
    Endpoint to get a list of questions.

    Args:
    request (Request): the request instance.
    params (QuestionParam): the question parameters to filter the questions. 

    Returns:
    List[Question]: a list of questions.
    """
    db_name = os.getenv("REACT_APP_DB")
    collection_name = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    domain = quiz.get("domain") or [1, 2]
    size = quiz.get("size") or 10
    pipeline = [
    {'$match': {'d': {'$eq': domain}}},
    {'$sample': {'size': size}}
    ]
    if quiz.get("s"):
        pipeline[0]["$match"].update({'$text': {'$search': f'\"{quiz.get("q")}\"'}})
    questions = await collection.aggregate(pipeline).to_list(size)
    random.shuffle(questions)
    # Convert _id field to string
    for question in questions:
        question["_id"] = str(question["_id"])
        
    # Get username from the session
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")

    # Get the user's session
    user_session = request.session.get(username, {"correct_count": 0})
    user_session["correct_count"] = 0

    # Save the user's session back to the main session
    request.session[username] = user_session

    return questions

@router.post("/validate")
async def validate(data: dict, request: Request):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")
    db_name = os.getenv("REACT_APP_DB")
    db_collections = os.getenv("REACT_APP_COLLECTIONS")
    db = client[db_name]
    collection = db[db_collections]
    document_id = data.get("document_id")
    answer = data.get("answer")

    # Get the user's session
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=400, detail="Invalid document ID")

    user_session = request.session.get(username, {"correct_count": 0})

    existing_data = await collection.find_one({"_id": ObjectId(document_id)})
    if existing_data:
        correct_answer = nlp(existing_data.get("a").lower())
        similarity_score = nlp(answer.lower()).similarity(correct_answer)
        if similarity_score > 0.85:
            user_session["correct_count"] += 1
            message = "Correct Answer"
        else:
            message = "Incorrect Answer"
            
    # Save the user's session back to the main session
    request.session[username] = user_session

    return {"message": message, "correct_count": user_session["correct_count"]}

@router.post("/results")
async def submit(request: Request):
    """
    Endpoint to submit the quiz and get the result.

    Args:
    request (Request): the request instance.

    Returns:
    dict: A dictionary with the count of correct answers for the user.
    """
    # Get username from the session
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")

    # Get the user's session
    user_session = request.session.get(username, {"correct_count": 0})

    # Extract the correct count from the user's session
    correct_count = user_session.get("correct_count", 0)

    # Clear the user's quiz data from the session after submission
    request.session[username] = user_session

    return {"message": "Quiz submitted successfully", "correct_count": correct_count}

@router.get("/check/{answer}")
async def check(answer: str, required: str):
    answer = nlp(answer)
    expected = nlp(required)
    similarity_score = answer.similarity(expected)
    return {"similarity": similarity_score}