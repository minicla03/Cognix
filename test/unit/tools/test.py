from rag_logic.tools.QATool import QATool
from rag_logic.tools.FlashcardTool import FlashcardTool
from rag_logic.tools.QuizTool import QuizTool
from rag_logic.tools.ITool import Context, ContextFactory


# ======================
# MOCK: Simulazione del sistema LangChain
# ======================

class MockVectorstore:
    """Simula un Vectorstore con documenti fittizi e punteggi di similarità."""
    def similarity_search_with_score(self, query, k=10):
        print(f"[Vectorstore] Ricerca similarità per query: '{query}' (k={k})")
        docs = [
            ("Documento 1: L'intelligenza artificiale è un campo dell'informatica.", 0.9),
            ("Documento 2: L'apprendimento automatico è una parte dell'IA.", 0.85),
            ("Documento 3: Le reti neurali sono modelli di ML ispirati al cervello umano.", 0.8),
        ]
        return docs[:k]


class MockRetriever:
    def __init__(self):
        self.vectorstore = MockVectorstore()


class MockCombineDocumentsChain:
    """Simula la generazione della risposta AI o la costruzione di output JSON."""
    def invoke(self, input):
        docs_text = "\n".join(str(d) for d in input.get("input_documents", []))
        question = input.get("question", "")
        return f"[LLM RESPONSE]\nPrompt:\n{question}\n\n[Context Used]\n{docs_text}"


class MockQAChain:
    def __init__(self):
        self.retriever = MockRetriever()
        self.combine_documents_chain = MockCombineDocumentsChain()


# ======================
# TEST DEL FLUSSO COMPLETO
# ======================

def main():
    # Simula un qa_chain completo
    qa_chain = MockQAChain()

    # Query di test
    query = {
        "user_query": "Spiega cos'è l'intelligenza artificiale e la differenza con l'apprendimento automatico.",
        "summary": "Abbiamo discusso di IA e machine learning in precedenza."
    }

    # Nomi strumenti da testare
    tools = ["qa_tool", "flashcard_tool", "quiz_tool"]

    for tool_name in tools:
        print(f"\n=======================")
        print(f" ESECUZIONE TOOL: {tool_name.upper()} ")
        print(f"=======================")

        # Crea dinamicamente il contesto con la factory
        context = ContextFactory.create(tool_name)
        if not context:
            print(f"[ERRORE] Impossibile creare tool '{tool_name}'")
            continue

        # Esegui il tool
        result = context.execute(qa_chain, query)

        # Mostra output sintetico
        print("\n[OUTPUT STRUTTURATO]")
        for k, v in result.items():
            print(f"{k}: {type(v).__name__}")

        print("\n[ESEMPIO OUTPUT DETTAGLIATO]")
        if "ai_response" in result:
            print(result["ai_response"])
        elif "result" in result:
            print(result["result"][:1])  # mostra solo il primo elemento per brevità


if __name__ == "__main__":
    main()
