from fastapi import APIRouter, Request, HTTPException, status
from typing import List, Optional

from pydantic import BaseModel, validator
from models.question import Question
from mongo.mongo import QUESTION_COLLECTION
from bson import ObjectId
from typing import Dict
import spacy
import random


router = APIRouter()

nlp = spacy.load("en_core_web_sm")

class UserStats(BaseModel):
    name: str
    questions: List[Question]
    result: List[str] = []
    score: int = 0
    
    @validator('result', pre=True)
    def make_result_set(cls, value):
        return list(set(value))

StatHolder: Dict[str, UserStats] = {}

@router.post("/questions/{user}", response_model=List[Question], status_code=200)
async def questions(user: str, quiz: Optional[dict] = {}):
    """
    Endpoint to get a list of questions.

    Args:
    request (Request): the request instance.
    params (QuestionParam): the question parameters to filter the questions. 

    Returns:
    List[Question]: a list of questions.
    """
    print(quiz)
    domain = quiz.get("domain") or [1, 2]
    size = quiz.get("size") or 10
    try:
        if domain[2] == 9:
            pipeline = [
                {'$match': {'d': {'$eq': domain[:2]}}},
                {'$sample': {'size': size}}
            ]
        elif domain[2] == 8:
            pipeline = [
                {'$match': {'d': {'$eq': domain}}},
                {'$sample': {'size': size}}
            ]
    except IndexError as e:
        pipeline = [
                {'$match': {'d': {'$eq': domain}}},
                {'$sample': {'size': size}}
            ]
    if quiz.get("s"):
        pipeline[0]["$match"].update({'$text': {'$search': f'\"{quiz.get("q")}\"'}})
    questions = await QUESTION_COLLECTION.aggregate(pipeline).to_list(size)
    random.shuffle(questions)
    if len(questions) == 0:
        pipeline[0]["$match"].update({'$text': {'$search': f'{quiz.get("q")}'}})
    questions: List[Question] = await QUESTION_COLLECTION.aggregate(pipeline).to_list(size)
    random.shuffle(questions)
    StatHolder[user] = UserStats(name=user, questions=questions)
    # Convert _id field to string

    for question in questions:
        question["a"] = ""
        question["_id"] = str(question["_id"])

    return questions

@router.post("/validate/{user}")
async def validate(user: str, data: dict):
    if user not in StatHolder:
        return HTTPException(status_code=400, detail="Quiz has not started or is not available")
    document_id = data.get("document_id")
    answer = data.get("answer")
    
    # Get the user's session
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=400, detail="Invalid document ID")

    for question in StatHolder[user].questions:
        if question.id == document_id:
            correct_answer = nlp(question.a.lower())
            similarity_score = nlp(answer.lower()).similarity(correct_answer)
            if similarity_score > 0.85:
                if question.id not in StatHolder[user].result:  # check if id is already in result list
                    StatHolder[user].result.append(question.id)
                    StatHolder[user].score = len(StatHolder[user].result)
            else:
                if question.id in StatHolder[user].result:
                    try:
                        StatHolder[user].result.remove(question.id)
                        StatHolder[user].score = len(StatHolder[user].result)
                    except ValueError as e:
                        pass
    print(StatHolder[user].score, StatHolder[user].result)
    return {"score": StatHolder[user].score}


@router.post("/results/{user}")
async def submit(user: str):
    """
    Endpoint to submit the quiz and get the result.

    Args:
    request (Request): the request instance.

    Returns:
    dict: A dictionary with the count of correct answers for the user.
    """
    # Get username from the session
    if user not in StatHolder:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz has not started or is not available")
    score = StatHolder[user].score
    result = StatHolder[user].result
    questions = StatHolder[user].questions
    del StatHolder[user]

    return {"message": "Quiz submitted successfully", "score": score, "result": result, "questions": questions}

@router.get("/check/{answer}")
async def check(answer: str, required: str):
    answer = nlp(answer)
    expected = nlp(required)
    similarity_score = answer.similarity(expected)
    return {"similarity": similarity_score}