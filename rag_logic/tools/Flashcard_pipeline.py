from rag_logic.tools.QA_pipeline import QAPipeline
from model.Flashcard import Flashcard
import json

class FlashcardPipeline(QAPipeline):
    def __init__(self):
        super().__init__()

    def execute(self, qa_chain, query, language_hint="italian", n_flashcard=10, difficulty = "medium"):
        """
        Crea un prompt per generare flashcard da un chunk di testo.

        Args:
            query: stringa con il contenuto da cui generare flashcard
            lang: lingua delle flashcard (es. "Italian", "English", "Spanish")
            n_cards: numero massimo di flashcard da generare
            difficulty: livello di difficoltà ("easy", "medium", "hard")

        Returns:
            flashcard: flashcard
        """

        _, filtered_docs = super(self).execute(qa_chain, query, language_hint) #TODO

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

        flashcards_text = qa_chain.combine_documents_chain.invoke(input={
            "input_documents": filtered_docs,
            "question": prompt
        })

        try:
            flashcards_data = json.loads(flashcards_text)
        except Exception:
            raise ValueError("Output non in formato JSON valido")

        flashcard = [Flashcard(answer=ft["answer"], question=ft["question"]) for ft in flashcards_data]

        return flashcard

