def quiz_generation(user_query, language_hint="italian", n_questions=5, difficulty="medium"):
    """
    Crea un prompt per generare quiz da un chunk di testo.

    text_chunk: testo da cui generare quiz
    lang: lingua delle domande (Italian, English, etc.)
    n_questions: numero di domande da generare
    difficulty: livello di difficoltà ("easy", "medium", "hard")
    """

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

    Text to process:
    {user_query}
    """

    return prompt
