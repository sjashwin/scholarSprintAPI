from fastapi import APIRouter
from typing import List
from models.quiz import Quiz
from mongo.mongo import QUIZ_COLLECTION
from typing import Optional
import logging

router = APIRouter()

async def fetch_data(query, collection, n):
    pipeline = [{'$match': query}, {'$sample': {'size': n}}]
    async for doc in collection.aggregate(pipeline):
        yield doc

async def get_quiz_from_db(n: int = 10):
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
    size = data.get("size")
    logging.debug(f"Fetching Quizzes")
    return await get_quiz_from_db(size)

@router.get("/preps", response_model=List[Quiz], status_code=200)
async def preps():
    pipeline = [{"$match": {"domain.2": 8}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(None)
    logging.debug(f"Getting Exam Preps Quiz.")
    return doc

@router.post("/getDomain/{domain}", response_model=List[Quiz], status_code=200)
async def getQuiz(domain: int): # 1 -> Natural Sciences
    pipeline = {"domain.0": domain}
    quiz = await QUIZ_COLLECTION.find(pipeline).to_list(None)
    logging.debug(f"Getting {domain} Quizzes")
    return quiz

@router.post('/searchQuiz', response_model=List[Quiz], status_code=200)
async def search_quiz(data: dict):
    phrase = str(data.get("phrase", ""))
    
    if not phrase:
        logging.info("Empty Search Request.")
        return await get_quiz_from_db()
    
    pipeline = [{"$match": {"$text": {"$search": phrase}}}]
    quiz = await QUIZ_COLLECTION.aggregate(pipeline).to_list(None)
    logging.info(f"with search phrase {phrase}")
    return quiz