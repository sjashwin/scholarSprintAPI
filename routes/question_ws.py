from fastapi import APIRouter, WebSocket
from fastapi import status
import spacy
from typing import Optional
from mongo.mongo import QUESTION_COLLECTION
import random

import json

router = APIRouter()

nlp = spacy.load("en_core_web_sm")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    data = await websocket.receive_json()
    questions = await getQuestions(data)
    client_questions = questions
    score = 0
    index = 0
    payload = {}
    payload = {
        "question": json.dumps(client_questions[index]),
        "index": index,
        "score": score,
        "size": len(client_questions),
    }
    for question in questions:
        question.setdefault('result', 0)
        question.setdefault('userAnswer', "")
    await websocket.send_json(payload)
    while True:
        data = await websocket.receive_json()
        if 'userAnswer' not in questions[index]:
            questions[index]['userAnswer'] = ""
        if 'validate' in data:
            answer = data["validate"]
            questions[index]["userAnswer"] = answer
            result = await validate(answer, client_questions[index]["a"])
            if result and questions[index]["result"] != 1:
                questions[index]["result"] = 1
                score += 1
            elif not result and question[index]["result"] == 1:
                score -= 1
                questions[index]["result"] = 0
            if data["type"] == "next" and index<len(questions):
                index += 1
            if data["type"] == "previous" and index > 0:
                index -= 1
            if data['type'] in "complete":
                payload = {
                    "complete": questions,
                    "score": score,
                }
                await websocket.send_json(payload)
                return
        try:
            payload = {
                "question": json.dumps(questions[index]),
                "index": index,
                "score": score,
            }
        except:
            payload = {
                "complete": questions,
                "score": score,
            }

        await websocket.send_json(payload)

async def getQuestions(quiz: Optional[dict] = {}):
    domain = quiz.get("domain") or [1, 2]
    size = quiz.get("size") or 10
    pipeline = [
    {'$match': {'d': {'$eq': domain[:2]}}},
    {'$sample': {'size': size}}
    ]
    if quiz.get("s"):
        pipeline[0]["$match"].update({'$text': {'$search': f'\"{quiz.get("q")}\"'}})
    questions = await QUESTION_COLLECTION.aggregate(pipeline).to_list(size)
    random.shuffle(questions)
    if len(questions) == 0:
        pipeline[0]["$match"].update({'$text': {'$search': f'{quiz.get("q")}'}})
    questions = await QUESTION_COLLECTION.aggregate(pipeline).to_list(size)
    random.shuffle(questions)
    # Convert _id field to string
    for question in questions:
        question["_id"] = str(question["_id"])
    # Get username from the session

    return questions

async def validate(given: str, required: str):
    return given == required