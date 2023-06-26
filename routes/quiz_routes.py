from fastapi import APIRouter
from typing import List
from models.quiz import Quiz
import os
from mongo.mongo import QUIZ_COLLECTION, QUESTION_COLLECTION
from typing import Optional
from models.question import Question

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
    quiz = []
    for i in range(1, 9):
        pipeline = [{'$match': {"domain.0": i}}, {'$sample': {'size': 10}}]
        doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(n)
        quiz.extend(doc)
    pipeline = [{'$match': {"domain.2": 8}}, {'$sample': {'size': 10}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(n)
    quiz.extend(doc)
    pipeline = [{'$match': {"domain.2": 9}}, {'$sample': {'size': 10}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(n)
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

@router.get("/preps", response_model=List[Quiz], status_code=200)
async def preps():
    pipeline = [{"$match": {"domain.2": 8}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(None)
    return doc

@router.post("/getDomain/{domain}", response_model=List[Quiz], status_code=200)
async def getQuiz(domain: int): # 1 -> Natural Sciences
    print(domain)
    pipeline = {"domain.0": domain}
    quiz = await QUIZ_COLLECTION.find(pipeline).to_list(None)
    return quiz

@router.post('/searchQuiz', response_model=List[Quiz], status_code=200)
async def searchQuiz(data: dict):
    phrase = str(data.get("phrase"))
    print(phrase)
    if len(phrase) == 0:
        return await get_quiz_from_db()
    quiz = []
    pipeline = { "$text": { "$search": phrase}}
    quiz = await QUIZ_COLLECTION.find(pipeline).to_list(None)
    return quiz