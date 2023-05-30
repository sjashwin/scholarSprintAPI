from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    answer: str
    domain: List[int]
    type_: int
    clue: str