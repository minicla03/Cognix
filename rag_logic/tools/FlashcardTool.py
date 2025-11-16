from abc import ABC

from rag_logic.tools.QATool import QATool
from persistence.model.Flashcard import Flashcard
import json

from rag_logic.utils import json_to_toon, toon_to_json


class FlashcardTool(QATool, ABC):
    def __init__(self):
        super().__init__()

    def execute(self, qa_chain, query, language_hint="italian", toon_format: bool = False, n_flashcard=10, difficulty = "medium"):
        """
        Crea un prompt per generare flashcard da un chunk di testo.

        Args:
            query: stringa con il contenuto da cui generare flashcard
            language_hint: lingua delle flashcard (es. "Italian", "English", "Spanish")
            n_flashcard: numero massimo di flashcard da generare
            difficulty: livello di difficoltà ("easy", "medium", "hard")

        Returns:
            flashcard: flashcard
        """

        response = super().execute(qa_chain, query, language_hint)
        filtered_docs = response["docs_source"]

        prompt = f"""
            You are an AI assistant that generates study flashcards from a given text. 
            The flashcards should help a student learn key concepts efficiently.
    
            Requirements:
            - Generate {n_flashcard} flashcards.
            - Each flashcard must have:
              - a clear question
              - a concise answer
            - Difficulty level: {difficulty}
            - Language: {language_hint}
            - Respond ONLY in valid JSON format as a list of objects:
              [
                {{"question": "...", "answer": "..."}},
                ...
              ]
    
            Text to process:
            {filtered_docs}
    
            Make sure questions are precise, answers are correct, and avoid extra commentary.
            """

        input_to_chain = {"input_documents": filtered_docs, "question": prompt}

        # Invoca il chain
        response = qa_chain.combine_documents_chain.invoke(input=input_to_chain,
            config=None,
            toon_format=toon_format
        )

        try:
            flashcards_data = json.loads(response)
        except Exception:
            raise ValueError("Output non in formato JSON valido")

        flashcard = [Flashcard(answer=ft["answer"], question=ft["question"]) for ft in flashcards_data]

        return {
            "type": "FLASHCARD",
            "result": flashcard,
            "docs_source": filtered_docs,
            "metadata": {
                "language": language_hint,
                "n_flashcards": n_flashcard,
                "difficulty": difficulty
            }
        }
