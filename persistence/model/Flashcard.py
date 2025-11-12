from dataclasses import dataclass

@dataclass
class Flashcard:
    id_notebook: str
    question: str
    answer: str

    def to_dict(self):
        return {
            'id_notebook': self.id_notebook,
            'question': self.question,
            'answer': self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Flashcard":
        return cls(
            id_notebook=data["id_notebook"],
            question=data["question"],
            answer=data["answer"],
        )