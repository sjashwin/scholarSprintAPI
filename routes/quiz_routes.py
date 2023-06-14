from fastapi import APIRouter
from typing import List
from models.quiz import Quiz
import os
from mongo.mongo import client
from typing import Optional

router = APIRouter()

def get_quiz_from_db(n: int = 20):
    """
    Function to fetch n number of quiz questions from the database.
    
    Args:
    n (int): Number of quiz questions to fetch. Default is 2.

    Returns:
    list: A list of Quiz instances.

    """
    db_name = os.getenv("REACT_APP_DB_QUIZ")
    collection_name = os.getenv("REACT_APP_QUIZ_COLLECTIONS")
    db = client[db_name]
    collection = db[collection_name]
    quiz = collection.find().to_list(n)
    
    return quiz

@router.get("/createquiz", response_model=List[Quiz], status_code=200)
async def create_quiz(data: Optional[dict] = {}):
    """
    Endpoint to create a quiz.
    
    This endpoint when called will fetch two quiz questions from the database and 
    return it as a list.

    Returns:
    list: A list of Quiz instances in JSON format.
    
    """
    size = data.get("size")
    return await get_quiz_from_db(size)