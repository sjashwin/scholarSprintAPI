from fastapi import APIRouter
from typing import List
from models.quiz import Quiz
import os
from mongo.mongo import client
from typing import Optional

router = APIRouter()

async def fetch_data(query, collection, n):
    pipeline = [{'$match': query}, {'$sample': {'size': n}}]
    async for doc in collection.aggregate(pipeline):
        yield doc

async def get_quiz_from_db(n: int = 10):
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
    quiz = []
    for i in range(1, 9):
        pipeline = [{'$match': {"domain.0": i}}, {'$sample': {'size': 10}}]
        doc = await collection.aggregate(pipeline).to_list(n)
        quiz.extend(doc)
    pipeline = [{'$match': {"domain.2": 9}}, {'$sample': {'size': 10}}]
    doc = await collection.aggregate(pipeline).to_list(n)
    quiz.extend(doc)

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