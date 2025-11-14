# Guida alla Contribuzione

Grazie per il tuo interesse nel contribuire a Q-AmodelAI! 🎉

Questo documento fornisce linee guida per contribuire al progetto.

---

## 📋 Indice

1. [Come Iniziare](#come-iniziare)
2. [Setup Ambiente di Sviluppo](#setup-ambiente-di-sviluppo)
3. [Workflow di Contribuzione](#workflow-di-contribuzione)
4. [Linee Guida per il Codice](#linee-guida-per-il-codice)
5. [Testing](#testing)
6. [Documentazione](#documentazione)
7. [Segnalazione Bug](#segnalazione-bug)
8. [Richieste di Funzionalità](#richieste-di-funzionalità)

---

## Come Iniziare

### Cosa puoi fare

- 🐛 **Bug Fix**: Correggi problemi esistenti
- ✨ **Nuove Features**: Aggiungi funzionalità
- 📚 **Documentazione**: Migliora docs e commenti
- 🧪 **Test**: Aggiungi test coverage
- 🎨 **UI/UX**: Migliora interfaccia Streamlit
- 🌍 **i18n**: Aggiungi supporto per nuove lingue

### Prerequisiti

- Conoscenza Python 3.10+
- Familiarità con Git/GitHub
- (Opzionale) Esperienza con LangChain, RAG, LLMs

---

## Setup Ambiente di Sviluppo

### 1. Fork e Clone

```bash
# Fork il repository su GitHub, poi:
git clone https://github.com/TUO_USERNAME/Q-AmodelAI.git
cd Q-AmodelAI

# Aggiungi upstream remote
git remote add upstream https://github.com/minicla03/Q-AmodelAI.git
```

### 2. Ambiente Virtuale

```bash
# Crea virtual environment
python -m venv venv

# Attiva (Linux/Mac)
source venv/bin/activate

# Attiva (Windows)
venv\Scripts\activate
```

### 3. Installa Dipendenze

```bash
# Dipendenze principali
pip install -r requirements.txt

# Dipendenze sviluppo (se esistono)
pip install -r requirements-dev.txt  # se presente

# Installa in modalità editable
pip install -e .
```

### 4. Setup Servizi

```bash
# MongoDB
mongod --dbpath ./data/mongodb

# Redis
redis-server

# Ollama
ollama serve
ollama pull llama3
```

### 5. Variabili d'Ambiente

Crea file `.env` nella root:

```bash
# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=rag_system_dev

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### 6. Verifica Setup

```bash
# Run tests
python -m pytest test/

# Start app
streamlit run presentation/notebook_page.py
```

---

## Workflow di Contribuzione

### 1. Sincronizza con Upstream

```bash
git checkout main
git fetch upstream
git merge upstream/main
```

### 2. Crea Branch Feature

```bash
# Usa naming convention:
# - feature/<nome-feature>
# - bugfix/<nome-bug>
# - docs/<nome-doc>

git checkout -b feature/new-document-loader
```

### 3. Sviluppo

- Scrivi codice pulito e ben commentato
- Segui le convenzioni del progetto
- Aggiungi test per nuove features
- Aggiorna documentazione se necessario

### 4. Commit

```bash
# Staging
git add <files>

# Commit con messaggio descrittivo
git commit -m "feat: Add support for DOCX document loading"

# Pattern per commit messages:
# feat: nuova funzionalità
# fix: correzione bug
# docs: documentazione
# test: aggiunta/modifica test
# refactor: refactoring codice
# style: formattazione, no logic change
# perf: miglioramento performance
```

### 5. Push e Pull Request

```bash
# Push su tuo fork
git push origin feature/new-document-loader

# Vai su GitHub e apri Pull Request
# - Descrivi le modifiche
# - Riferisci issue correlate (#123)
# - Aggiungi screenshot se UI changes
```

### 6. Code Review

- Rispondi ai commenti dei reviewer
- Apporta modifiche richieste
- Mantieni la discussione costruttiva

### 7. Merge

Dopo approvazione, un maintainer farà merge della PR.

---

## Linee Guida per il Codice

### Style Guide

#### Python (PEP 8)

```python
# Buono ✅
def load_document(file_path: str, encoding: str = "utf-8") -> List[str]:
    """
    Load document from file path.
    
    Args:
        file_path: Path to document file
        encoding: File encoding (default: utf-8)
        
    Returns:
        List of document chunks
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
    
    return split_into_chunks(content)


# Evita ❌
def ld(fp,enc="utf-8"):
    f=open(fp,'r',encoding=enc)
    c=f.read()
    f.close()
    return c.split('\n\n')
```

### Naming Conventions

```python
# Classi: PascalCase
class DocumentLoader:
    pass

# Funzioni/metodi: snake_case
def load_and_process():
    pass

# Costanti: UPPER_SNAKE_CASE
MAX_CHUNK_SIZE = 600

# Variabili: snake_case
user_query = "question"
```

### Type Hints

```python
from typing import List, Dict, Optional

def process_query(
    query: str,
    max_results: int = 10,
    language: Optional[str] = None
) -> Dict[str, any]:
    """Usa sempre type hints per parametri e return"""
    pass
```

### Docstrings

```python
def complex_function(param1: str, param2: int) -> bool:
    """
    Breve descrizione funzione (una riga).
    
    Descrizione più dettagliata se necessario.
    Può essere multi-riga.
    
    Args:
        param1: Descrizione primo parametro
        param2: Descrizione secondo parametro
        
    Returns:
        Descrizione valore di ritorno
        
    Raises:
        ValueError: Quando param2 < 0
        
    Example:
        >>> complex_function("test", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return len(param1) > param2
```

### Imports

```python
# Standard library
import os
import sys
from typing import List, Dict

# Third party
import streamlit as st
from langchain_core.messages import HumanMessage

# Local
from rag_logic.agents import routing_agent
from persistence.mongo import UserRepository
```

### Error Handling

```python
# Buono ✅
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise
except Exception as e:
    logger.exception("Unexpected error")
    # Handle or re-raise

# Evita ❌
try:
    result = risky_operation()
except:
    pass  # Silent fail - molto male!
```

---

## Testing

### Struttura Test

```
test/
├── unit/
│   ├── agents/
│   ├── ingestion/
│   └── tools/
├── integration/
└── fixtures/
```

### Scrivere Test

```python
import pytest
from rag_logic.tools.QATool import QATool

class TestQATool:
    @pytest.fixture
    def qa_tool(self):
        """Setup test fixture"""
        return QATool()
    
    def test_execute_with_valid_query(self, qa_tool):
        """Test case description"""
        # Arrange
        query = {"user_query": "What is Python?", "summary": ""}
        
        # Act
        result = qa_tool.execute(mock_chain, query)
        
        # Assert
        assert result["type"] == "QA"
        assert "ai_response" in result
        assert len(result["docs_source"]) > 0
    
    def test_execute_with_no_results(self, qa_tool):
        """Test edge case"""
        query = {"user_query": "very obscure query", "summary": ""}
        result = qa_tool.execute(mock_chain, query)
        
        assert result["ai_response"] == "Informazione non presente nel contesto."
```

### Eseguire Test

```bash
# Tutti i test
pytest

# Con coverage
pytest --cov=rag_logic --cov-report=html

# Specifico modulo
pytest test/unit/agents/

# Specifico test
pytest test/unit/agents/test_router.py::TestRouter::test_classification
```

### Test Coverage

- Punta a >80% coverage per nuovo codice
- Testa happy path e edge cases
- Include error conditions

---

## Documentazione

### README.md

Aggiorna README se aggiungi:
- Nuove features principali
- Nuovi requisiti/dipendenze
- Modifiche setup/installazione

### ARCHITECTURE.md

Aggiorna se modifichi:
- Struttura componenti
- Flussi di dati
- Pattern implementati

### Docstrings

- Obbligatori per funzioni pubbliche
- Segui format Google/NumPy style
- Include esempi se utile

### Code Comments

```python
# Buono ✅ - Spiega il PERCHÉ
# Usiamo threshold=0.75 perché test mostrano che sotto
# questo valore le risposte diventano poco affidabili
filtered_docs = filter_by_similarity(docs, threshold=0.75)

# Inutile ❌ - Spiega il COSA (già ovvio dal codice)
# Incrementa contatore di uno
counter += 1
```

---

## Segnalazione Bug

### Prima di Segnalare

1. Cerca issue esistenti
2. Verifica con ultima versione
3. Prova a riprodurre in ambiente pulito

### Template Issue

```markdown
**Descrizione Bug**
Breve descrizione del problema.

**Riproduzione**
Step per riprodurre:
1. Vai a '...'
2. Clicca su '...'
3. Vedi errore

**Comportamento Atteso**
Cosa ti aspettavi succedesse.

**Comportamento Attuale**
Cosa succede invece.

**Screenshots**
Se applicabile.

**Ambiente**
- OS: [es. Ubuntu 22.04]
- Python: [es. 3.10.5]
- Versione Q-AmodelAI: [es. commit hash]

**Log/Traceback**
```
[Paste error traceback qui]
```

**Informazioni Aggiuntive**
Altro contesto utile.
```

---

## Richieste di Funzionalità

### Template Feature Request

```markdown
**Funzionalità Proposta**
Descrizione chiara della feature.

**Motivazione**
Perché questa feature è utile? Che problema risolve?

**Soluzione Proposta**
Come vorresti che funzionasse?

**Alternative Considerate**
Altre soluzioni che hai valutato.

**Informazioni Aggiuntive**
Mockups, esempi, riferimenti.
```

---

## Aree di Contribuzione

### 🟢 Good First Issues

- Aggiungere docstrings mancanti
- Migliorare error messages
- Piccoli bug fix
- Aggiornare documentazione

### 🟡 Intermediate

- Nuovi document loaders (DOCX, TXT, Markdown)
- Miglioramenti UI Streamlit
- Nuove metriche di valutazione
- Ottimizzazioni performance

### 🔴 Advanced

- Nuovo tool per RAG
- Sistema di autenticazione
- Deployment Docker
- Scalabilità distribuita

---

## Code Review Checklist

Prima di submittare PR, verifica:

- [ ] Codice segue style guide
- [ ] Test aggiunti/aggiornati
- [ ] Test passano tutti
- [ ] Documentazione aggiornata
- [ ] No hardcoded secrets/credentials
- [ ] Commit messages descrittivi
- [ ] Branch aggiornato con main
- [ ] PR description completa

---

## Domande?

- 💬 Apri una Discussion su GitHub
- 📧 Contatta maintainer
- 📚 Leggi [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Codice di Condotta

### Aspettative

- Sii rispettoso e costruttivo
- Accetta feedback con mente aperta
- Focus su cosa è meglio per il progetto
- Mostra empatia verso altri contributors

### Non Accettabile

- Linguaggio offensivo
- Attacchi personali
- Trolling o commenti provocatori
- Comportamento non professionale

---

## Riconoscimenti

Tutti i contributors saranno riconosciuti in:
- README.md (Contributors section)
- Release notes per contributi significativi

---

**Grazie per contribuire a Q-AmodelAI! 🚀**

*Documento aggiornato: Novembre 2025*
