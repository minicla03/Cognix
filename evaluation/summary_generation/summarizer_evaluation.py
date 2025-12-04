import logging

from deepeval.evaluate import evaluate
from deepeval.test_case import LLMTestCase

from rag_logic.agents.summarizer_agent import summary_agent
from rag_logic.utils import detect_language_from_query

from evaluation.summary_generation.summary_testset import  TEST_CASE
from evaluation.summary_generation.summary_metrics import *

logger = logging.getLogger(__name__)

import json
from pathlib import Path
from html import escape


def generate_html_report(results, output_path="summarizer_report.html"):
    """
    Genera un report HTML dai risultati della valutazione dei sommari.

    Args:
        results: lista di dizionari restituiti da evaluate_summarizer
        output_path: percorso file HTML da creare
    """
    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Summarizer Evaluation Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
            th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            pre { white-space: pre-wrap; word-wrap: break-word; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>Summarizer Evaluation Report</h1>
        <table>
            <tr>
                <th>Test Index</th>
                <th>Predicted Summary</th>
                <th>Expected Summary</th>
                <th>Classic Metrics</th>
                <th>DeepEval Metrics</th>
            </tr>
    """

    for r in results:
        html_content += f"""
        <tr>
            <td>{r['test_index']}</td>
            <td><pre>{escape(r['predicted_summary'])}</pre></td>
            <td><pre>{escape(r['expected_summary'])}</pre></td>
            <td><pre>{escape(json.dumps(r['classic_metrics'], indent=2, ensure_ascii=False))}</pre></td>
            <td><pre>{escape(json.dumps(r['deepeval'], indent=2, ensure_ascii=False))}</pre></td>
        </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # Scrive il file HTML
    Path(output_path).write_text(html_content, encoding="utf-8")
    print(f"Report HTML generato: {output_path}")

def evaluate_summarizer(test_dataset):

    toon_format_options = [False]
    results = []

    for idx, item in enumerate(test_dataset):

        conversation_history = item["conversation_history"]
        expected_summary = item["expected_summary"]

        language_hint = detect_language_from_query(conversation_history[0]["content"])
        logger.info(f"Language hint: {language_hint}")
        item_result = {}

        for toon_format in toon_format_options:

            predicted = summary_agent(conversation_history, False, language_hint)

            conv_text = "\n".join(f"{msg['role']}: {msg['content']}" for msg in conversation_history)

            ctx = [f"{msg['role']}: {msg['content']}" for msg in conversation_history]

            test_case = LLMTestCase(
                input=conv_text,
                actual_output=predicted,
                expected_output=expected_summary,
                context= ctx,
                retrieval_context= ctx
            )

            logger.info("Avvio valutazione DeepEval sul summarizer...")
            deepeval_result = evaluate(test_cases=[test_case], metrics=summary_metrics.get_list_deep_eval_metrics())

            classic_metric_result = summary_metrics.classic_metric(expected_summary, predicted)

            results.append({
                "test_index": idx,
                "toon_format": toon_format,
                "predicted_summary": predicted,
                "expected_summary": expected_summary,
                "deepeval": deepeval_result,
                "classic_metrics": classic_metric_result
            })

    return results

def start_evaluation_summarizer():
    dataset = TEST_CASE
    results = evaluate_summarizer(dataset)
    generate_html_report(results, output_path="report.html")
