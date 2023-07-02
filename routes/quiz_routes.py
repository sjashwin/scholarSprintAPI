from fastapi import APIRouter
from typing import List
from models.quiz import Quiz
from mongo.mongo import QUIZ_COLLECTION
from typing import Optional
import logging
import asyncio

router = APIRouter()

async def fetch_quiz_by_domain(domain: int, n: int):
    pipeline = [{'$match': {'domain.0': domain}}, {'$sample': {'size': n}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(n)
    return doc

async def get_quiz_from_db(n: int = 10):
    quiz = []
    domains = list(range(1, 9))
    tasks = [fetch_quiz_by_domain(domain, n) for domain in domains]
    quiz_results = await asyncio.gather(*tasks)
    quiz.extend([item for sublist in quiz_results for item in sublist])
    pipeline = [{'$match': {"domain.2": 8}}, {'$sample': {'size': n}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(n)
    quiz.extend(doc)
    pipeline = [{'$match': {"domain.2": 9}}, {'$sample': {'size': n}}]
    doc = await QUIZ_COLLECTION.aggregate(pipeline).to_list(n)
    quiz.extend(doc)

    return quiz

@router.get("/createquiz", response_model=List[Quiz], status_code=200)
async def create_quiz(data: Optional[dict] = {}):
    size = data.get("size") or 10
    logging.debug(f"Fetching Quizzes")
    return await get_quiz_from_db(int(size))

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