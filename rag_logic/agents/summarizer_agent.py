import logging
from rag_logic.llm.LLM import LLM

# Configura logger di base
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def summary_agent(conversation_history: list, toon_format=False, language_hint="italian"):
    logger.info("Avvio generazione sommario...")
    logger.info("Lunghezza conversazione: %d messaggi", len(conversation_history))

    # Converte la conversazione in testo
    conv_text = "\n".join(
        f"{type(msg).__name__}: {msg.content}" if hasattr(msg, "content") else str(msg)
        for msg in conversation_history
    )
    logger.info("Conversazione convertita in testo. Lunghezza caratteri: %d", len(conv_text))

    # Prepara prompt per LLM
    prompt_summary = f"""
        You are a chat summarization agent. 
        Your task is to analyze the entire conversation history between the user and the assistant 
        and produce a clear, concise summary capturing the essential information.\n\n

        Guidelines:\n
        - Write in {language_hint}.\n
        - Focus on the main topics discussed, the user’s goals, and any specific requests or constraints.\n
        - Omit greetings, filler phrases, or unrelated small talk.\n
        - Maintain a neutral and factual tone.\n
        - If the conversation includes technical explanations, summarize the key points without unnecessary detail.\n\n

        Your output should be a short paragraph (5–7 lines) that provides enough context
        for another model to understand what the conversation was about and continue it smoothly.\n\n
    """
    logger.info("Prompt preparato per il modello. Lunghezza caratteri: %d", len(prompt_summary))

    messages = [
        {"role": "system", "content": prompt_summary},
        {"role": "user", "content": conv_text}
    ]

    logger.info("Invio messaggi al modello LLM (toon_format=%s)...", toon_format)
    summary = LLM().invoke(messages, config=None, toon_format=toon_format)
    logger.info("Sommario generato correttamente. Lunghezza caratteri: %d %s", len(summary), type(summary))

    logger.debug("Sommario:\n%s", summary)
    return summary
