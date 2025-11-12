from dataclasses import dataclass
from typing import List

@dataclass
class Quiz:
    id_notebook: str
    question: str
    answer_list: List[str]
    difficulty: str
    correct_answer: str

    def to_dict(self):
        return {
            'id_notebook': self.id_notebook,
            'question': self.question,
            'answer_list': self.answer_list,
            'difficulty': self.difficulty,
            'correct_answer': self.correct_answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        return cls(
            id_notebook=data["id_notebook"],
            question=data["question"],
            answer_list=data["answer_list"],
            difficulty=data["difficulty"],
            correct_answer=data["correct_answer"]
        )


