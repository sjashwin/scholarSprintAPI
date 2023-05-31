from pydantic import BaseModel
from models.question import Questions
from typing import List

class Quiz(BaseModel):
    time: int
    questions: List[Questions]