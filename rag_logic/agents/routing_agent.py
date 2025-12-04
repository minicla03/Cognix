import logging
import re

from rag_logic.llm.LLM import LLM

logger = logging.getLogger(__name__)

def router_agent(user_query, toon_format, language_hint="italian"):
    """
    Route the user's query to the appropriate RAG subsystem (QA, Flashcard, or Quiz).

    This function uses an LLM (via LLM) to analyze the intent of the user's request
    and decide which internal tool should handle it.

    Parameters
    ----------
    user_query : str
        The user's input or question.
    language_hint : str, optional
        The expected language of the user query (default is "italian").
        This helps the model understand linguistic context and phrasing.

    Returns
    -------
    str
        The name of the function to execute.
        Possible values:
        - "QA_TOOL" → for explanatory or informational queries.
        - "FLASHCARD_TOOL" → for flashcard generation requests.
        - "QUIZ_TOOL" → for quiz or study-question generation requests.

    Notes
    -----
    - The model is instructed to output only one of the three possible tool names.
    - The output is normalized to handle small variations (e.g., extra spaces or text).
    - Uses a low temperature to ensure deterministic classification.
    """

    logger.info("Avvio router_agent per query: %s", user_query)

    prompt_routing = f"""
        You are an intelligent task router for a Retrieval-Augmented Generation (RAG) system.
        Your job is to analyze the user's request and decide which function should be executed.
        
        Available functions:
        1. QA_TOOL → Answers a question based on the context retrieved from documents.
        2. FLASHCARD_TOOL → Generates study flashcards (question/answer pairs) from the content.
        3. QUIZ_TOOL → Generates quiz from the content.
        
        Guidelines:
        - Use the language of the user's query if detectable, otherwise fallback to {language_hint}.
        - If the query asks for explanations, summaries, or answers → QA_TOOL.
        - If the query asks to generate flashcards → FLASHCARD_TOOL.
        - If the query asks to generate quiz questions → QUIZ_TOOL.
        - If multiple intents are present, choose the one explicitly requested last.
        
        Few-shot examples:
        - User (Italian): Spiegami MQTT → QA_TOOL
        - User (Italian): Crea flashcards su MQTT → FLASHCARD_TOOL
        - User (English): Make study flashcards for Edge computing → FLASHCARD_TOOL
        - User (Spanish): ¿Cuál es la diferencia entre Edge y Fog? → QA_TOOL
        - User (French): Explique-moi HTTPS → QA_TOOL
        - User (German): Erstelle Lernkarten über RAM und ROM → FLASHCARD_TOOL
        
        Respond ONLY with one of: QA_TOOL, FLASHCARD_TOOL, QUIZ_TOOL. No extra text, punctuation, or explanation.
    """

    messages = [
        {"role": "system", "content": prompt_routing},
        {"role": "user", "content": user_query}
    ]

    try:
        response = LLM().invoke(
            input=messages,
            config=None,
            toon_format=toon_format
        )

        #(model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40)
        logger.info("Invio messaggi al modello LLM...")

        text = response.strip().upper() #.content
        logger.info("Risposta grezza del modello: %s", text)

        match = re.search(r"(QA_TOOL|FLASHCARD_TOOL|QUIZ_TOOL)", text)
        if match:
            tool = match.group(1)
            logger.info("Tool selezionato: %s", tool)
            return tool

        logger.warning("Nessuna corrispondenza valida trovata nel testo: %s", text)
        logger.info("Default → QA_TOOL")

        return "QA_TOOL"
    except Exception as error:
        logger.error("Errore durante il routing: %s", str(error))
        logger.debug("Traceback completo:", exc_info=True)
        return "QA_TOOL"