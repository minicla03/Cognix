import re

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
import logging

logger = logging.getLogger(__name__)

def router_agent(user_query, language_hint="italian"):
    """
    Route the user's query to the appropriate RAG subsystem (QA, Flashcard, or Quiz).

    This function uses an LLM (via Ollama) to analyze the intent of the user's request
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
        "You are an intelligent task router for a Retrieval-Augmented Generation (RAG) system."
        "Your job is to analyze the user's request and decide which function should be executed."
    
        "Available functions:"
        "1. QA_TOOL → Answers a question based on the context retrieved from documents."
        "2. FLASHCARD_TOOL → Generates study flashcards (question/answer pairs) from the content."
        "3. QUIZ_TOOL → Generates quiz from the content."
        
        "Guidelines:"
        "- Use the language of the user request ({language_hint})."
        "- If the user asks for explanations, answers, summaries → QA_TOOL."
        "- If the user asks to generate flashcards → FLASHCARD_TOOL."
        "- If the user asks to generate quiz, questions for study → QUIZ_TOOL."
        
        "Instructions:"
        "- If the user asks for explanations, summaries, or answers → choose QA_TOOL."
        "- If the user explicitly asks to create, generate, or build flashcards, summaries for study, or Q/A pairs → choose FLASHCARD_TOOL."
        "- If the user asks to create, generate or build quiz, questions for study  → QUIZ_TOOL."
        "- Respond ONLY with the name of the function to call, nothing else."
        
        "Few-shot examples:"
        "-User (Italian): Spiegami come funziona il protocollo MQTT. → QA_TOOL"
        "-User (Italian): Crea delle flashcard sul protocollo MQTT per ripassare. → FLASHCARD_TOOL"
        "-User (English): Make study flashcards for the chapter on Edge computing. → FLASHCARD_TOOL"
        "-User (Spanish): ¿Cuál es la diferencia entre Edge y Fog computing? → QA_TOOL"
                
        Response only with the name of tool to use: QA_TOOL, FLASHCARD_TOOL, QUIZ_TOOL.
        Do not add text, explanations, or punctuation.
    """

    messages = [
        SystemMessage(content=prompt_routing),
        HumanMessage(content=user_query)
    ]

    try:

        llm = ChatOllama(model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40)
        logger.info("Invio messaggi al modello Ollama...")

        response = llm.invoke(messages)
        text = response.content.strip().upper()
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