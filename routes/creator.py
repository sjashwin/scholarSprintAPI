from fastapi import APIRouter
from models.quiz import Quiz
from typing import List
from models.question import Question
from mongo.mongo import QUESTION_COLLECTION, USERQUIZ_COLLECTION
import json
router = APIRouter()

@router.get("/creator/quiz")
async def createNewQuiz(userID: str):
    quiz = Quiz(
        time=90,
        image="",
        size=10,
        name="Default Quiz",
        domain=[],
        s=False,
        q="",
        quesID=[],
        userID=userID
    )

    return quiz

@router.post("/creator/question/search", response_model=List[Question])
async def search(data: dict):
    print(data)
    domain = data.get("domain") or 1
    subDomain = data.get("subDomain") or 2
    questions = await QUESTION_COLLECTION.find({"d": [domain, subDomain]}).to_list(10)
    return questions

@router.post("/creator/submit")
async def submit(data: dict):
    name = data.get("name")
    time = data.get("time")
    domain = data.get("domain")
    image = data.get("image") or ""
    type_ = data.get("type") or 1
    size = data.get("size") or 10
    type_ = data.get("type") or 1
    s = data.get("s") or False
    q = data.get("q") or ""
    quesID = data.get("quesID")
    userID = data.get("userID")
    data = Quiz(
        time=time,
        image=image,
        name=name,
        size=size,
        type=type_,
        domain=domain,
        quesID=quesID,
        userID=userID
    )
    result = await USERQUIZ_COLLECTION.insert_one(data.dict())
    return {"inserted_id": str(result.inserted_id)}

@router.post("/creator/quiz/modify/{quizID}")
async def modify(quizID: str):
    pass

@router.get("/creator/{userID}", response_model=List[Quiz])
async def quiz(userID: str):
    quiz = await USERQUIZ_COLLECTION.find({ "userID": userID}).to_list(None)
    return quiz