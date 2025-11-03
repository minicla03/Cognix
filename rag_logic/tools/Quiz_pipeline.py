from rag_logic.tools.QA_pipeline import QAPipeline
from model.Quiz import Quiz
import json


class QuizPipeline(QAPipeline):
    def __init__(self):
        super(self).__init__()

    def execute(self, qa_chain, query: str, language_hint: str = "italian", n_questions=5, difficulty="medium"):

        _, filtered_docs = super(self).execute(qa_chain, query, language_hint) #TODO

        prompt = f"""
        You are an AI assistant that generates multiple-choice quiz questions from a given text.

        Requirements:
        - Generate {n_questions} quiz questions.
        - Each quiz must have:
            - "question": a clear question
            - "answer_list": a list of 3-4 possible answers
            - "correct_answer": the correct answer (must be one of the options in answer_list)
            - "difficulty": "{difficulty}"
        - Language: {language_hint}
        - Respond ONLY in valid JSON format as a list of objects with the fields: question, answer_list, correct_answer, difficulty
        - answer_list must include 3-4 options: one correct answer and 2-3 plausible distractors it the uses choose hard difficulty. 
        - Avoid obviously wrong answers.
        - Do not include extra commentary or explanations.

        Text to process: {query}
        """

        quiz_text = qa_chain.combine_documents_chain.invoke(input={
            "input_documents": filtered_docs,
            "question": prompt
        })

        try:
            quiz_data = json.loads(quiz_text)
        except Exception:
            raise ValueError("Output non in formato JSON valido")

        quiz = [Quiz(question=qt["question"],answer_list=qt["answer_list"], correct_answer=qt["correct_answer"], difficulty=qt["difficulty"])
                for qt in quiz_data]

        return {
            "type": "QUIZ",
            "result": quiz,
            "docs_source": filtered_docs,
            "metadata": {"language": language_hint, "n_questions": n_questions, "difficulty": difficulty}
        }
