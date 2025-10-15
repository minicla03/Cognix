from dataclasses import dataclass
from typing import List

@dataclass
class Quiz:
    question: str
    answer_list: List[str]
    difficulty: str
    correct_answer: str


