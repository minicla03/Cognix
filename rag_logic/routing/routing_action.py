from langchain_ollama import ChatOllama

from rag_logic.tools.ITool import Context
from rag_logic.tools.Flashcard_pipeline import FlashcardPipeline
from rag_logic.tools.QA_pipeline import QAPipeline
from rag_logic.tools.Quiz_pipeline import QuizPipeline

def router(qa_chain, user_query, language_hint="italian"):
    """
    Funzione per il routing dell'operazione che LLM deve svolgere.
    Si basa su un routing agent-base

    Args:
        user_query: string, prompt utente
        language_hint: string, lingua del prompt
        qa_chain: QAChain,

    Returns:
        answer: string risposta da parte del LLM
    """

    prompt =(
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

        "User query: {user_query}")

    llm = ChatOllama(model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40)
    response = llm.chat(messages=[{"role": "user", "content": prompt}])

    context = None
    if response == "QA_TOOL": context = Context(QAPipeline())
    elif response == "FLASHCARD_TOOL": context = Context(FlashcardPipeline())
    elif response == "QUIZ_TOOL": context = Context(QuizPipeline())

    try:
        return context.execute(qa_chain, user_query, language_hint)
    except BaseException as be:
        raise be.with_traceback()
