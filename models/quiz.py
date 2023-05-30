from typing import List, Optional
from pydantic import BaseModel
from .question import Question
from .user import User
import json

class Results(BaseModel):
    user: User
    score: int = 0

class Quiz(BaseModel):
    questions: List[Question] = []
    timer: Optional[int] = None
    users: List[User] = []
    results: List[Results]

    def __init__(self):
        for user in self.users:
            self.results.append(Results(user=user))

    def create_questions(self, data: Optional[dict] = None):
        with open('physics.json') as json_file:
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
            self.add_question(question) # Adding questions

    def add_question(self, question: Question):
        self.questions.append(question)

    def check(self, index: int, answer: str, user_id: str):
        # Find the Results object for the user who answered the question
        result_for_user = next((result for result in self.results if result.user.id == user_id), None)
        if result_for_user is None:
            # Handle the case where the user is not in results (this should not normally happen)
            raise ValueError(f"No results found for user with ID {user_id}")

        # Check if the user's answer is correct
        if self.questions[index].answer == answer:
            result_for_user.score += 1

