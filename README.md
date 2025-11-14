# Q-AmodelAI

Sistema di domanda e risposta (QA) multilingue basato su documenti PDF caricati dall'utente, con interfaccia web tramite Streamlit.

---

## 💡 Descrizione

**Q-AmodelAI** è un sistema RAG (Retrieval-Augmented Generation) avanzato che combina:
- 🤖 Agenti intelligenti per routing automatico delle query
- 📚 Gestione notebook per organizzare documenti e conversazioni
- 🧠 Tre modalità di interazione: QA, Flashcard, Quiz
- 🌍 Supporto multilingua completo (IT, EN, ES, FR, DE)
- 💾 Architettura persistente con MongoDB e Redis
- 📊 Sistema di valutazione con metriche NLP avanzate

Funzionalità principali:
- Caricare PDF e CSV tramite interfaccia web Streamlit
- Eseguire domande sui contenuti con risposte contestualizzate
- Generare flashcard per lo studio
- Creare quiz di verifica automatici
- Gestire cronologia chat con summarization
- Organizzare documenti in notebook tematici

---

## ⚙️ Requisiti

### Software richiesto
- Python 3.10+
- [Ollama](https://ollama.com/) installato e attivo con modello `llama3:latest`
- MongoDB (per persistenza dati)
- Redis (per cache e sessioni temporanee)

### Librerie Python
Le dipendenze principali includono:
- `langchain`, `langchain-ollama`, `langchain-chroma`
- `streamlit` (interfaccia web)
- `pymongo` (MongoDB client)
- `redis` (Redis client)
- `sentence-transformers` (embeddings)

---

## 📦 Installazione

```bash
# Clona il repository
git clone https://github.com/minicla03/Q-AmodelAI.git
cd Q-AmodelAI

# (Opzionale) Crea un ambiente virtuale
python -m venv venv
source venv/bin/activate      # Su Windows: venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# Avvia i servizi necessari (in terminali separati)

# 1. Avvia MongoDB
mongod --dbpath /path/to/your/data/db

# 2. Avvia Redis
redis-server

# 3. Avvia Ollama con Llama3
ollama run llama3
```

**Configurazione opzionale via variabili d'ambiente:**
```bash
export MONGO_HOST=localhost
export MONGO_PORT=27017
export MONGO_DB=rag_system
export REDIS_HOST=localhost
export REDIS_PORT=6379
```

---

## 🚀 Avvio dell'interfaccia grafica

L'applicazione utilizza **Streamlit** come framework per l'interfaccia web.

```bash
# Avvia la pagina principale dei notebook
streamlit run presentation/notebook_page.py

# Oppure avvia direttamente la chat (richiede notebook_id)
streamlit run presentation/pages/chat.py
```

**Note:**
- La prima volta, assicurati che MongoDB e Redis siano in esecuzione
- L'app creerà automaticamente le cartelle necessarie (`docs/`, `chroma_db/`)

---

## 📂 Struttura cartelle

```
Q-AmodelAI/
├── rag_logic/           # Logica RAG (Retrieval-Augmented Generation)
├── persistence/         # Layer di persistenza dati
├── presentation/        # Interfaccia utente (Streamlit)
├── evaluation/          # Script e dati per la valutazione del sistema
├── test/                # Test unitari
└── docs/                # Documenti caricati dall'utente (generato a runtime)
```

---

## 🔍 Componenti principali

### 📁 `rag_logic/` - Logica RAG

| Sottocartella | Descrizione |
|---------------|-------------|
| `agents/` | Agenti intelligenti per routing e summarization |
| `ingestion/` | Caricamento e processamento documenti (PDF, CSV) |
| `tools/` | Strumenti specializzati (QA, Flashcard, Quiz) |
| `memory/` | Gestione cronologia chat e notebook |
| `qa_utils.py` | Utility per rilevamento lingua e pulizia testo |

**Agenti principali:**
- `routing_agent.py`: Instrada le query agli strumenti appropriati
- `summarizer_agent.py`: Genera riassunti delle conversazioni

**Tools disponibili:**
- `QATool`: Risponde a domande basate sui documenti
- `FlashcardTool`: Genera flashcard per lo studio
- `QuizTool`: Crea quiz di verifica

### 📁 `persistence/` - Layer di Persistenza

| Sottocartella | Descrizione |
|---------------|-------------|
| `IxRepository/` | Interfacce repository (pattern Repository) |
| `model/` | Modelli dati (User, Chat, Notebook, Flashcard, Quiz) |
| `mongo/` | Implementazione repository con MongoDB |
| `redis/` | Implementazione repository con Redis (dati temporanei) |

**Architettura:**
- MongoDB per dati persistenti (utenti, notebook, flashcard, quiz)
- Redis per dati temporanei (sessioni chat)
- Pattern Repository per astrazione accesso dati

### 📁 `presentation/` - Interfaccia Utente

| File | Descrizione |
|------|-------------|
| `pages/chat.py` | Pagina principale chat con Streamlit |
| `notebook_page.py` | Gestione notebook utente |

**Framework:** Streamlit per interfaccia web interattiva

### 📁 `evaluation/` - Sistema di Valutazione

| File | Descrizione |
|------|-------------|
| `evaluation.py` | Script di valutazione con memoria |
| `evaluation_no_memory.py` | Valutazione senza contesto storico |
| `summary_evaluation.py` | Riepilogo risultati valutazione |
| `test_case.py` | Definizione test case |
| `data/` | Dataset per testing |

---


## 📊 Valutazione del sistema QA

Per testare il sistema su un insieme di domande con risposte attese:

```bash
python evaluation_no_memory.py
```

Salverà un file `metriche_medie.txt` con le metriche F1, BLEU, ROUGE-L, Similarità semantica, Precision/Recall contestuali.

---

## 🏗️ Architettura del Sistema

### Flusso di Funzionamento

1. **Ingestion**: Documenti (PDF, CSV) vengono caricati e processati
   - Parsing del contenuto
   - Chunking del testo (600 caratteri, overlap 200)
   - Generazione embeddings multilingua (HuggingFace)
   - Persistenza in ChromaDB (vector store)

2. **Routing**: L'utente invia una query
   - `routing_agent` analizza l'intento
   - Determina quale tool utilizzare (QA, Flashcard, Quiz)

3. **Retrieval**: Il tool appropriato recupera informazioni
   - Similarity search nel vector store
   - Filtraggio per soglia di similarità
   - Selezione dei documenti più rilevanti

4. **Generation**: Costruzione della risposta
   - LLM (Llama3) genera risposta basata sui documenti
   - Supporto multilingua (rilevamento automatico)
   - Inclusione fonti utilizzate

5. **Memory**: Gestione del contesto
   - Chat history salvata in Redis (temporaneo)
   - Notebook e metadata in MongoDB (persistente)
   - Summarization per conversazioni lunghe

### Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| LLM | Ollama (Llama3:latest) |
| Embeddings | HuggingFace (paraphrase-multilingual-MiniLM-L12-v2) |
| Vector Store | ChromaDB |
| DB Persistente | MongoDB |
| Cache/Sessioni | Redis |
| Framework RAG | LangChain |
| UI | Streamlit |
| Testing | Python unittest, metriche NLP (BLEU, ROUGE, F1) |

---

## 🗃️ Gestione documenti

- ✅ Carica PDF: tramite GUI
- ✅ Mostra documenti: pulsante dedicato
- 🔜 Cancellazione documenti: da implementare in futuro

---

## 🌐 Supporto multilingua

Lingue supportate (rilevamento automatico o esplicitazione nella query):

- Italiano
- Inglese
- Spagnolo
- Francese
- Tedesco

---

## 🧪 Esempio d’uso

1. Carica uno o più PDF (es. appunti universitari)
2. Inserisci una domanda nella GUI, ad es.:
   - `Spiega il pattern Observer in italiano`
   - `What is an oscilloscope?`
3. Ottieni una risposta sintetica, chiara, con fonti utilizzate
