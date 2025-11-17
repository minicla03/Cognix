from typing import Dict, List
import json

import nltk
import numpy as np
from deepeval.metrics import SummarizationMetric, GEval, HallucinationMetric
from langchain_community.embeddings import OpenAIEmbeddings
from scipy.stats import cosine

"""
Kryscinski et al. (2019) proposed four dimensions for evaluating abstractive summaries:

Fluency: Each sentence should be well-formed and free of grammatical errors or random capitalization that makes it hard to read
Coherence: Collective quality of all sentences, where the summary should be well-structured and not just a heap of information
Relevance: Picking the important aspects from the source document to include in the summary and excluding the rest
Consistency: The summary and source document should be factually consistent aka faithful (i.e., no new information in the summary that’s not in the source)
"""

def get_fluency_metric():
    # alignment and coverage. These correspond closely to the precision and recall

    return SummarizationMetric(
        verbose_mode=True,
        n=20,
        truths_extraction_limit=20,
    )


def get_consistency_metric(llm):
    """
    Consistency / Faithfulness: il sommario non deve introdurre informazioni false.
    Usare LLM per confronto sommario vs testo originale.
    """
    def consistency_fn(summary: str, reference: str) -> float:
        prompt = (
            "Sei un valutatore. Controlla se il seguente sommario "
            "è coerente con il testo originale. Restituisci un punteggio tra 0 e 1.\n\n"
            f"Testo originale:\n{reference}\n\n"
            f"Sommario:\n{summary}\n\n"
            "Rispondi solo con il punteggio float tra 0 e 1."
        )
        response = llm.invoke({"role": "user", "content": prompt})
        try:
            score = float(response)
        except:
            score = 0.0
        return score

    return CustomMetric(
        name="Consistency",
        fn=consistency_fn,
        requires=["ACTUAL_OUTPUT", "REFERENCE"]
    )

def get_repetitiveness_metric():
    repetitiveness_metric = GEval(
        name="Repetitiveness",
        criteria="""I do not want my summary to contain unnecessary repetitive information.
        Return 1 if the summary does not contain unnecessarily repetitive information, and 0 if the summary contains unnecessary repetitive information.
        facts or main points that are repeated more than once. Points on the same topic, but talking about different aspects, are OK. In your reasoning, point out any unnecessarily repetitive points.""",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        verbose_mode=True
    )
    return repetitiveness_metric

def compute_coherence_score(sentences):
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    sentences_embeddings = embedding_model.embed_documents(sentences)
    sentence_similarities = []
    for i in range(len(sentences_embeddings) - 2):
    # Convert embeddings to numpy arrays and reshape to 2D
    emb1 = np.array(sentences_embeddings[i])
    emb2 = np.array(sentences_embeddings[i+2])
    # Calculate cosine distance
    distance = cosine(emb1, emb2)
    similarity = 1 - distance
    sentence_similarities.append(similarity)
    coherence_score = np.mean(sentence_similarities)
    return coherence_score

def get_vagueness_metric(llm):
    def judge_vague(sentences: List[str], j=None) -> float:
        prompt = (
            "Sei un valutatore. Ti do una lista di frasi, valuta per ciascuna se è vaga.\n"
            "Le frasi vaghe non esplicitano punti chiave.\n"
            "Rispondi con JSON: [{\"sentence\": ..., \"is_vague\": true/false, \"reason\": …}, …]"
        )
        response = llm.invoke({"role": "user", "content": prompt + "\n\n" + "\n".join(sentences)})
        data = json.loads(response)
        vague_count = sum(1 for x in data["sentences"] if x["is_vague"])
        return 1.0 - (vague_count / len(sentences))

    return CustomMetric(name="Vagueness", fn=judge_vague, requires=["ACTUAL_OUTPUT"])


import nltk
import spacy
nlp = spacy.load("en_core_web_sm")

def get_entity_density(text):
    summary_tokens = nltk.word_tokenize(text)
    num_tokens = len(summary_tokens)
    doc = nlp(text)
    num_entities = len(doc.ents)
    entity_density = num_entities / num_tokens
    return entity_density


def aggregate_results(result: Dict[str, float], weights: Dict[str, float]) -> float:
    total = 0.0
    w_sum = 0.0
    for metric_name, score in result.items():
        w = weights.get(metric_name, 1.0)
        total += w * score
        w_sum += w
    return total / w_sum if w_sum > 0 else 0.0