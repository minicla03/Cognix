import re
from typing import Any, Dict, Literal

from toon_format import encode, decode, EncodeOptions, DecodeOptions

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
    """
    Detects the language of a user query based on keywords and language names.

    Returns:
        str: language key (e.g., 'italian', 'english') or None if not detected
    """
    query_lower = query.lower()
    for lang, aliases in LANGUAGE_ALIASES.items():
        for alias in aliases:
            patterns = [
                rf"\b(in|in lingua)\s+{re.escape(alias)}\b",
                rf"rispondi in {re.escape(alias)}",
                rf"\b{re.escape(alias)}\b"
            ]
            if any(re.search(pat, query_lower) for pat in patterns):
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
