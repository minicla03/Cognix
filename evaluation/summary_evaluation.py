import logging

from langchain_core.messages import HumanMessage, SystemMessage
from sentence_transformers import util, SentenceTransformer
from langchain_ollama import ChatOllama

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def evaluate_summary(conversation_history: list, summary: str, language_hint="italian"):
    """ Evaluates a summary without human reference.
    Returns:
        - semantic similarity: score from 0 to 1
        - factuality_score: score from 0 to 1 estimated by the LLM """

    logger.info("Preparing conversation text...")
    conv_text = "\n".join(
        f"{type(msg).__name__}: {msg.content}" if hasattr(msg, "content") else str(msg)
        for msg in conversation_history
    )

    logger.info("Computing semantic similarity...")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    emb_conv = model.encode(conv_text, convert_to_tensor=True)
    emb_summary = model.encode(summary, convert_to_tensor=True)
    semantic_similarity = util.cos_sim(emb_conv, emb_summary).item()  # 0-1

    logger.info(f"Semantic similarity computed: {semantic_similarity:.3f}")
    logger.info("Evaluating factuality with LLM...")

    prompt_summary = f"""
    "You are a chat summarization agent. "
    "Your task is to analyze the entire conversation history between the user and the assistant "
    "and produce a clear, concise summary capturing the essential information.\n\n"

    "Guidelines:\n"
    "- Write in {language_hint}.\n"
    "- Focus on the main topics discussed, the user’s goals, and any specific requests or constraints.\n"
    "- Omit greetings, filler phrases, or unrelated small talk.\n"
    "- Maintain a neutral and factual tone.\n"
    "- If the conversation includes technical explanations, summarize the key points without unnecessary detail.\n\n"

    "Your output should be a short paragraph (5–7 lines) that provides enough context "
    "for another model to understand what the conversation was about and continue it smoothly.\n\n"
    """

    messages = [
        SystemMessage(content=prompt_summary),
        HumanMessage(conv_text)
    ]

    llm = ChatOllama(model="llama3:latest", temperature=0.0)
    response = llm.invoke(messages)
    try:
        factuality_score = float(response.content.strip())
    except ValueError:
        factuality_score = None
        logger.warning(f"LLM did not return a numeric score: {response.content}")

    logger.info(f"Factuality score: {factuality_score}")
    return {
        "semantic_similarity": semantic_similarity,
        "factuality_score": factuality_score
    }

if __name__ == "__main__":

    chat_history = [
        HumanMessage(content="Ciao, voglio capire come funzionano le reti neurali e i loro principali componenti."),
        SystemMessage(content="Certo! Una rete neurale è composta da strati di neuroni artificiali. Gli strati principali sono input, hidden e output. Ogni neurone calcola una funzione sul input e passa il risultato allo strato successivo."),
        HumanMessage(content="Quali sono gli algoritmi principali per addestrarle?"),
        SystemMessage(content="Il metodo più comune è il backpropagation, che aggiorna i pesi della rete minimizzando l'errore. Altri algoritmi includono ottimizzatori come SGD, Adam e RMSprop."),
        HumanMessage(content="E per problemi di classificazione immagini?"),
        SystemMessage(content="Per le immagini si usano tipicamente reti convoluzionali (CNN), che applicano filtri per rilevare caratteristiche locali come bordi e texture."),
        HumanMessage(content="Perfetto, puoi fare un breve riepilogo di tutto quello che abbiamo detto?")
    ]

    summary = ("L'utente ha chiesto spiegazioni sulle reti neurali. L'assistente ha spiegato la struttura (input, hidden, output), "
               "il funzionamento dei neuroni, l'addestramento tramite backpropagation e ottimizzatori come SGD, Adam, RMSprop. "
               "Ha menzionato anche le CNN per la classificazione delle immagini.")

    scores = evaluate_summary(chat_history, summary)
    logger.info(f"Evaluation results: {scores}")
