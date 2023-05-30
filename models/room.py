from typing import List, Optional
from pydantic import BaseModel
from .user import User
from .question import Question
from .quiz import Quiz
from typing import List
import uuid, json, random

class Room(BaseModel):
    id: str = str(uuid.uuid4())
    img: Optional[str] = None
    quiz: Quiz
    size: Optional[int] = 5
    clue: bool = False
    users: List[User] = []

    def set_quiz(self):
        with open('physics.json', 'r') as json_file:
            data = json.load(json_file)
        for index, item in enumerate(data):
            if index >= 5:
                break
            question = Question(
                question=item["q"],
                answer=item["a"],
                domain=item["d"],
                type_=item["t"],
                clue=item["c"]
            )
            self.quiz.add_question(question)
        random.shuffle(self.quiz)

RoomWarehouse: List[Room] = []