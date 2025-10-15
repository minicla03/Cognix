def generate_flash_card_argument(query, language_hint="italian", n_cards = 5, difficulty = "medium"):
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

    prompt = f"""
        You are an AI assistant that generates study flashcards from a given text. 
        The flashcards should help a student learn key concepts efficiently.

        Requirements:
        - Generate {n_cards} flashcards.
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
        {query}

        Make sure questions are precise, answers are correct, and avoid extra commentary.
        """

    response =

    return flashcard