from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Union
from user import User
from question import Question
import uuid

class Result:
    i: int
    result: Union[int, str, bool]

class Room(BaseModel):
    id = str(uuid.uuid4())
    user: List[User]
    questions: List[Question]
    results: List[Result]
    userID: str

QUESTION_LIMIT = 20

router = APIRouter()

rooms: List[Room] = []

@router.post("/room/{userID}")
async def rooms(userID: str):
    Room(
        user=[], 
        userID=userID, 
        results=[],
        questions=[]
    )
    pass

@router.post("/room/addQuestion")
async def rooms(data: dict):
    roomID = data.get("roomID")
    question = data.get("question")



@router.get("/question/{id}")
async def questions():
    pass

@router.post("/answer/{id}/{userID}")
async def answer(id: str, userID: str, answer: dict):
    pass

@router.post("/complete/{id}")
async def complete():
    pass