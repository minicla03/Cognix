"""
Funzioni di utilità per la gestione delle domande e risposte.
Queste funzioni includono:
- detect_language_from_query: per rilevare la lingua della domanda basata su parole chiave.
- clean_text: per pulire il testo rimuovendo spazi e caratteri non necessari.
- LANGUAGE_ALIASES: un dizionario per mappare le lingue a nomi alternativi.
"""

import re

from toon_format import encode, decode, EncodeOptions, DecodeOptions
from typing import Any, Dict, Literal

LANGUAGE_ALIASES = {
    "italian": ["italiano", "italian"],
    "english": ["inglese", "english"],
    "french": ["francese", "french"],
    "spanish": ["spagnolo", "spanish"],
    "german": ["tedesco", "german"]
}

def clean_text(text):
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = ' '.join(text.split())
    return text.split

def detect_language_from_query(query):
    query_lower = query.lower()
    for lang, aliases in LANGUAGE_ALIASES.items():
        for alias in aliases:
            if re.search(r"\b(in|in lingua)\s+" + re.escape(alias) + r"\b", query_lower) or f"rispondi in {alias}" in query_lower:
                return lang
    return None

def json_to_toon(data: Dict[str, Any], *,
                 delimiter: str = ",",
                 indent: int = 2,
                 length_marker: Literal["#", False] = "#") -> str:
    """
    Converte un dict JSON in una stringa TOON usando toon‑python.

    Args:
        data: dict da serializzare
        delimiter: delimitatore per array (default ",")
        indent: spazi per livello indentazione (default 2)
        length_marker: prefisso lunghezza array (default "")

    Returns:
        stringa TOON
    """

    options: EncodeOptions = {
        "indent": indent,
        "delimiter": delimiter,
        "lengthMarker": length_marker
    }
    toon_str = encode(data, options=options)
    return toon_str


def toon_to_json(toon_str: str, *, indent: int = 2, strict: bool = True) -> Any:
    """
    Converte una stringa TOON in un oggetto Python (dict/list) usando toon‑python.

    Args:
        toon_str: stringa TOON da deserializzare
        indent: indentazione attesa (default 2)
        strict: se attivare il parsing rigoroso (default True)

    Returns:
        oggetto Python risultante (dict, list, etc)
    """
    options: DecodeOptions = DecodeOptions(indent=indent, strict=strict)
    obj = decode(toon_str, options=options)
    return obj
