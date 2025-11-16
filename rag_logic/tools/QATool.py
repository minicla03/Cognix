from rag_logic.tools.ITool import IToolStrategy


class QATool(IToolStrategy):

    def __init__(self):
        super().__init__()

    def execute(self, qa_chain, query: dict, language_hint="italian", toon_format: bool = False, max_sources=3, similarity_threshold=0.75):

        # Esegue una ricerca nel vectorstore per ottenere i documenti pertinenti ricercando per similarità
        user_query = query["user_query"]
        summary = query["summary"]

        vectorstore = qa_chain.retriever.vectorstore
        retrieved_docs_with_scores = vectorstore.similarity_search_with_score(user_query, k=10)

        # Filtra i documenti recuperati in base alla soglia di similarità
        filtered_docs_with_scores = [(doc, score) for doc, score in retrieved_docs_with_scores if
                                     score >= similarity_threshold]
        # Limita il numero di documenti a quelli richiesti
        filtered_docs_with_scores = filtered_docs_with_scores[:max_sources]
        # Estrae solo i documenti filtrati
        filtered_docs = [doc for doc, _ in filtered_docs_with_scores]

        if not filtered_docs:
            return {
                "type": "QA",
                "ai_response": "Informazione non presente nel contesto.",
                "docs_source": [],
                "metadata": {"language": language_hint, "max_sources": max_sources}
            }

        # Prepara il prompt per la generazione della risposta
        prompt = f"""
            Answer in {language_hint} clearly and simply,
            explaining the main concepts in a way that’s easy to understand even for non-experts.
            The answer should include the essential details, such as definitions and key characteristics,
            but without using overly technical or complex language.
            Be concise yet complete, as if you were explaining the topic to a student or colleague who wants to fully understand it.\n\n
            Question: {user_query}
            Rely exclusively on the information provided in the context to construct an accurate and complete answer.
        """

        if summary:
            prompt += f"\nConsider also the history of the chat: {summary}"

        input_to_chain = {
                "input_documents": filtered_docs,
                "question": prompt
            }

        # Combina i documenti recuperati e il prompt per generare la risposta
        response = qa_chain.combine_documents_chain.invoke(
            input=input_to_chain,
            config=None,
            toon_format=toon_format
        )

        return  {
            "type": "QA",
            "ai_response": response ,
            "docs_source": filtered_docs,
            "metadata": {"language": language_hint, "max_sources": max_sources}
        }
