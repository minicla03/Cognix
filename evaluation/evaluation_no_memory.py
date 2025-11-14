"""
Script per valutare un sistema di domande e risposte su un set di test predefinito.
Utilizza il QASystemManager per gestire le operazioni QA e calcola le metriche di performance.
"""

from rag_logic.ChatManager import ChatManager
from evaluation import evaluate_all, compute_context_precision_recall
from test_case import TEST_CASES

# Inizializza il gestore del sistema QA
manager = ChatManager()

if not manager._is_ready():
    print("QA System non pronto.")
    exit()

print("Inizio valutazione su test set...\n")

# Lista per memorizzare i risultati delle metriche
results = []

with open("metriche_medie.txt", "w", encoding="utf-8") as f:
    '''
    Esegue i test definiti in TEST_CASES e calcola le metriche di performance.
    I risultati vengono stampati a console e salvati in un file di testo.
    '''
    for idx, test in enumerate(TEST_CASES, 1):
        query = test["query"]
        expected = test["expected_answer"]
        lang = test.get("language_hint", "italian")
        relevant_docs = test.get("relevant_docs", [])

        prediction, source_docs = manager.ask(query, language=lang)
        # Filtra i documenti pertinenti in base ai metadati
        if isinstance(prediction, dict):
            output_text = prediction.get("output_text", "")
        else:
            output_text = str(prediction)
        retrieved_sources = [doc.metadata.get("source") for doc in source_docs if doc.metadata.get("source")]

        # Calcola le metriche di performance
        qa_scores = evaluate_all(output_text, expected, language=lang)
        context_precision, context_recall = compute_context_precision_recall(retrieved_sources, relevant_docs)

        qa_scores["Context Precision"] = context_precision
        qa_scores["Context Recall"] = context_recall
        results.append(qa_scores)

        print(f"Test #{idx}")
        print(f"Domanda: {query}")
        print(f"Risposta attesa: {expected}")
        print(f"Risposta modello: {output_text}")
        print("Metriche:")
        for key, value in qa_scores.items():
            print(f"    - {key}: {value:.3f}" if isinstance(value, float) else f"    - {key}: {value}")
        print("-" * 60)

        f.write(f"Test #{idx}\n")
        f.write(f"Domanda: {query}\n")
        f.write(f"Risposta attesa:\n{expected}\n")
        f.write(f"Risposta modello:\n{output_text}\n")
        f.write("Metriche:\n")
        for key, value in qa_scores.items():
            f.write(f"  - {key}: {value:.3f}\n" if isinstance(value, float) else f"  - {key}: {value}\n")
        f.write("-" * 60 + "\n\n")

    if results:
        f.write("\nMetriche medie su tutti i test:\n\n")
        avg = {key: sum(r[key] for r in results) / len(results) for key in results[0]}
        for key, value in avg.items():
            f.write(f"{key}: {value:.3f}\n")

        print("\nMetriche medie su tutti i test:")
        for key, value in avg.items():
            print(f"  {key}: {value:.3f}")

