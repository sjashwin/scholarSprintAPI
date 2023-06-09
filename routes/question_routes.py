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
    questions = await collection.find(params).to_list(2)

    # Convert _id field to string
    for question in questions:
        question["_id"] = str(question["_id"])
        
    # Get username from the session
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")

    # Get the user's session
    user_session = request.session.get(username, {"questions": [], "correct_count": 0})

    # Map the quiz to the username and add it to the user's session
    user_session["questions"] = [q for q in questions]

    # Save the user's session back to the main session
    request.session[username] = user_session

    return questions

@router.post("/validate/{index}/{answer}")
async def validate(index: int, answer: str, request: Request):
    """
    Endpoint to validate the answer for a given question.

    Args:
    index (int): The index of the question in the session.
    answer (str): The answer provided by the user.

    Returns:
    dict: A dictionary with the message indicating whether the answer was correct and
          the updated count of correct answers for the user.
    """
    # Get username from the session
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")

    # Get the user's session
    user_session = request.session.get(username, {"questions": [], "correct_count": 0})

    # Validate question index
    if index >= len(user_session["questions"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid question index")

    # Retrieve the question from the user's session
    question = user_session["questions"][index]
    print(question)

    # Check the answer
    if question["a"][0].lower() == answer.lower():
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
    user_session = request.session.get(username, {"questions": [], "correct_count": 0})

    # Extract the correct count from the user's session
    correct_count = user_session.get("correct_count", 0)

    # Clear the user's quiz data from the session after submission
    user_session["questions"] = []
    user_session["correct_count"] = 0
    request.session[username] = user_session

    return {"message": "Quiz submitted successfully", "correct_count": correct_count}