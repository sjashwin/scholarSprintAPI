from typing import List, Optional
from pydantic import BaseModel, Field, BaseSettings
from .question import Question
from .user import User
import os
from pymongo import MongoClient

client = MongoClient(os.getenv("REACT_APP_MONGO_HOST"))
db = client[os.getenv("REACT_APP_DB")]
collections = db[os.getenv("REACT_APP_COLLECTIONS")]

class Settings(BaseSettings):
    arbitrary_types_allowed = True

class Results(BaseModel):
    user: User
    score: int = 0

class Quiz(BaseModel):
    questions: List[Question] = Field(default_factory=list)
    timer: int = 0
    users: List[User] = Field(default_factory=list)
    results: List[Results] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        for user in self.users:
            self.results.append(Results(user=user))
    
    class Config(Settings):
        pass

    def create_questions(self, data: Optional[dict] = None):
        self.questions = list(collections.find().limit(10))
