from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

_semantic_model = None

def get_semantic_model():
    global _semantic_model
    if _semantic_model is None:
        _semantic_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return _semantic_model

def compute_f1(prediction, ground_truth, language='italian'):
    """
    Calcola l'F1 Score tra la previsione e la risposta attesa.
    L'F1 Score è la media armonica tra precision e recall:
    - Precision: frazione di token predetti corretti
    - Recall: frazione di token di riferimento catturati
    Utilizza il tokenization per gestire le differenze linguistiche.
    Args:
        prediction (str): La risposta generata dal modello.
        ground_truth (str): La risposta corretta attesa.
        language (str): La lingua della risposta, usata per la tokenizzazione.
    Returns:
        float: L'F1 Score calcolato tra la previsione e la risposta attesa.
    """
    pred_tokens = tokenizer.tokenize(prediction.lower())
    gt_tokens = tokenizer.tokenize(ground_truth.lower())
    common = set(pred_tokens) & set(gt_tokens)
    if len(common) == 0:
        return 0.0
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gt_tokens)
    return 2 * (precision * recall) / (precision + recall)

def compute_bleu(prediction, ground_truth, language='italian'):
    """
    Calcola il BLEU Score tra la previsione e la risposta attesa.
    Misura la precisione n-gram tra predizione e riferimento
    - Penalizza risposte troppo brevi
    - Tiene conto della posizione delle parole
    - Smoothing per evitare punteggi zero
    Args:
        prediction (str): La risposta generata dal modello.
        ground_truth (str): La risposta corretta attesa.
        language (str): La lingua della risposta, usata per la tokenizzazione.
    Returns:
        float: Il BLEU Score calcolato tra la previsione e la risposta attesa.
    """
    reference = [tokenizer.tokenize(ground_truth.lower())]
    hypothesis = tokenizer.tokenize(prediction.lower())
    smooth = SmoothingFunction().method1
    return sentence_bleu(reference, hypothesis, smoothing_function=smooth)

def compute_rouge(prediction, ground_truth):
    """
    Calcola il ROUGE-L Score tra la previsione e la risposta attesa.
    Misura la corrispondenza della sequenza più lunga comune:
    - Considera l'ordine delle parole
    - Meno sensibile a riarrangiamenti che BLEU
    - Particolarmente utile per riassunti
    Args:
        prediction (str): La risposta generata dal modello.
        ground_truth (str): La risposta corretta attesa.
    Returns:
        float: Il ROUGE-L Score calcolato tra la previsione e la risposta attesa.
    """
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(ground_truth, prediction)
    return scores['rougeL'].fmeasure
    
def custom_metrics(prediction, ground_truth, language='italian'):
    return {
        "F1": compute_f1(prediction, ground_truth, language=language),
        "BLEU": compute_bleu(prediction, ground_truth, language=language),
        "ROUGE-L": compute_rouge(prediction, ground_truth),
    }
