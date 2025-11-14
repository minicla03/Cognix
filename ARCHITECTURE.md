# Architettura Q-AmodelAI

Documentazione tecnica dettagliata dell'architettura del sistema Q-AmodelAI.

---

## 📋 Indice

1. [Panoramica](#panoramica)
2. [Architettura a Livelli](#architettura-a-livelli)
3. [Flusso dei Dati](#flusso-dei-dati)
4. [Componenti Chiave](#componenti-chiave)
5. [Pattern e Principi](#pattern-e-principi)
6. [Tecnologie Utilizzate](#tecnologie-utilizzate)

---

## Panoramica

Q-AmodelAI è un sistema RAG (Retrieval-Augmented Generation) modulare che implementa un'architettura multi-layer per la gestione di documenti, l'elaborazione di query e la generazione di contenuti educativi.

### Caratteristiche Architetturali

- **Modularità**: Componenti ben separati con responsabilità chiare
- **Scalabilità**: Supporto per multiple sessioni e utenti
- **Persistenza**: Dual-storage (MongoDB + Redis) per dati persistenti e temporanei
- **Estensibilità**: Pattern Strategy per aggiungere nuovi loader e tool
- **Multilingua**: Supporto nativo per 5 lingue

---

## Architettura a Livelli

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Streamlit)          │
│  - notebook_page.py (gestione notebook)         │
│  - pages/chat.py (interfaccia chat)             │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│            RAG LOGIC LAYER                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   AGENTS     │  │    TOOLS     │            │
│  │ - routing    │  │ - QATool     │            │
│  │ - summarizer │  │ - Flashcard  │            │
│  └──────────────┘  │ - Quiz       │            │
│                    └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  INGESTION   │  │   MEMORY     │            │
│  │ - PDF/CSV    │  │ - ChatMgr    │            │
│  │ - Chunking   │  │ - Notebook   │            │
│  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│          PERSISTENCE LAYER                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   MongoDB    │  │    Redis     │            │
│  │ - Users      │  │ - Sessions   │            │
│  │ - Notebooks  │  │ - Chat Hist  │            │
│  │ - Flashcards │  │              │            │
│  │ - Quizzes    │  │              │            │
│  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│          EXTERNAL SERVICES                      │
│  - Ollama (LLM - Llama3)                        │
│  - ChromaDB (Vector Store)                      │
│  - HuggingFace (Embeddings)                     │
└─────────────────────────────────────────────────┘
```

---

## Flusso dei Dati

### 1. Ingestion Flow (Caricamento Documenti)

```
User Upload (PDF/CSV)
    ↓
DocumentLoaderStrategy (pattern Strategy)
    ↓
Document Parsing
    ↓
RecursiveCharacterTextSplitter
    ├─ chunk_size: 600
    └─ chunk_overlap: 200
    ↓
HuggingFace Embeddings
    └─ paraphrase-multilingual-MiniLM-L12-v2
    ↓
ChromaDB Vector Store
    └─ collection: user_{user_id}_notebook_{notebook_id}
```

### 2. Query Flow (Elaborazione Query)

```
User Query
    ↓
routing_agent (LLM-based classification)
    ├─ Analizza intento
    └─ Seleziona tool appropriato
    ↓
┌─────────┬─────────────┬──────────┐
│  QATool │ FlashcardTool│ QuizTool │
└─────────┴─────────────┴──────────┘
    ↓
Similarity Search (ChromaDB)
    ├─ k=10 documenti
    └─ similarity_threshold=0.75
    ↓
LLM Generation (Ollama Llama3)
    ├─ Context: documenti rilevanti
    ├─ Query: domanda utente
    └─ Chat history: riassunto conversazione
    ↓
Response + Sources
    ↓
ChatHistory (Redis) + Summarization (se necessario)
```

### 3. Memory Management Flow

```
Chat Messages
    ↓
ChatManager
    ├─ Salva in Redis (temporaneo)
    └─ Ogni N messaggi → Summarization
    ↓
summarizer_agent
    └─ Genera riassunto conversazione
    ↓
MongoDB (persistente)
    └─ Aggiorna metadata notebook
```

---

## Componenti Chiave

### 1. rag_logic/agents/

#### routing_agent.py
**Responsabilità**: Classificazione automatica delle query

```python
def router_agent(user_query, language_hint="italian") -> str:
    """
    Returns: "QA_TOOL" | "FLASHCARD_TOOL" | "QUIZ_TOOL"
    """
```

**Funzionamento**:
- Utilizza Ollama (Llama3) per analizzare l'intento
- Temperature bassa (0.1) per classificazione deterministica
- Prompt engineering per output strutturato

#### summarizer_agent.py
**Responsabilità**: Riassunto conversazioni lunghe

**Trigger**: Quando la chat supera una certa lunghezza

---

### 2. rag_logic/tools/

Implementano `IToolStrategy` (pattern Strategy)

#### QATool
- **Input**: query utente + riassunto chat
- **Output**: risposta + documenti fonte
- **Parametri**:
  - `max_sources=3`: massimo documenti da utilizzare
  - `similarity_threshold=0.75`: soglia minima similarità

#### FlashcardTool
- **Output**: Set di flashcard (domanda/risposta)
- **Formato**: JSON strutturato

#### QuizTool
- **Output**: Quiz a scelta multipla
- **Formato**: JSON con domanda, opzioni, risposta corretta

---

### 3. rag_logic/ingestion/

#### DocumentLoaderStrategy (Pattern Strategy)
```python
IDocumentLoader (Interface)
    ├─ PDFLoader
    └─ CSVLoader
```

**Estensibilità**: Aggiungere nuovi loader implementando `IDocumentLoader`

#### IngestionFlow
**Responsabilità**: Orchestrazione processo ingestion

**Steps**:
1. Load document via strategy
2. Split in chunks
3. Generate embeddings
4. Store in ChromaDB

---

### 4. rag_logic/memory/

#### ChatManager
**Responsabilità**: Gestione cronologia conversazioni

**Funzioni principali**:
- `add_message()`: aggiunge messaggio a storia
- `get_history()`: recupera storia chat
- `summarize_if_needed()`: trigger summarization

**Storage**: Redis (temporaneo, performance)

#### NotebookManager
**Responsabilità**: Gestione notebook utente

**Funzioni principali**:
- `create_notebook()`: crea nuovo notebook
- `get_notebooks()`: lista notebook utente
- `update_metadata()`: aggiorna info notebook

**Storage**: MongoDB (persistente)

---

### 5. persistence/

#### Pattern Repository
Astrazione accesso dati con interfacce:
- `IUserRepository`
- `IChatRepository`
- `INotebookRepository`
- `IFlashcardRepository`
- `IQuizRepository`

#### MongoDB Implementation
**Collections**:
- `users`: dati utente
- `notebooks`: metadata notebook
- `flashcards`: flashcard generate
- `quizzes`: quiz generati

**Vantaggi**:
- Schema flessibile per documenti
- Queries complesse su metadata
- Persistenza a lungo termine

#### Redis Implementation
**Keys Pattern**: `chat:{chat_id}:messages`

**Vantaggi**:
- Accesso ultra-rapido
- TTL automatico per cleanup
- Ideale per sessioni temporanee

---

### 6. presentation/

#### Streamlit Architecture
**Multi-page app**:
- `notebook_page.py`: Home page
- `pages/chat.py`: Chat interface

**Session State**:
- `current_notebook_id`
- `chat_manager`
- `messages`

**Layout**:
```
┌─────────┬─────────┬─────────┐
│  Docs   │  Chat   │  Tools  │
│ Upload  │ History │ Export  │
└─────────┴─────────┴─────────┘
```

---

## Pattern e Principi

### Design Patterns Utilizzati

1. **Strategy Pattern**
   - Loader per documenti
   - Tools per elaborazione query
   
2. **Repository Pattern**
   - Astrazione layer persistenza
   - Facile switch tra DB
   
3. **Singleton Pattern**
   - Connection managers (MongoDB, Redis)
   - Evita connessioni multiple
   
4. **Factory Pattern**
   - Creazione embeddings
   - Inizializzazione chains

### Principi SOLID

- **Single Responsibility**: Ogni classe ha una responsabilità ben definita
- **Open/Closed**: Estensibile via Strategy (nuovi loader/tools)
- **Dependency Inversion**: Dipendenze su interfacce, non implementazioni

---

## Tecnologie Utilizzate

### Core Technologies

| Tecnologia | Versione | Utilizzo |
|------------|----------|----------|
| Python | 3.10+ | Linguaggio principale |
| LangChain | Latest | Framework RAG |
| Streamlit | Latest | Web UI |
| MongoDB | 5.0+ | Database persistente |
| Redis | 6.0+ | Cache & sessions |

### AI/ML Stack

| Componente | Modello/Servizio | Scopo |
|------------|------------------|-------|
| LLM | Ollama Llama3 | Generazione risposte |
| Embeddings | HuggingFace MiniLM-L12-v2 | Rappresentazione semantica |
| Vector DB | ChromaDB | Similarity search |

### Libraries

```python
# RAG & LLM
langchain>=0.1.0
langchain-ollama
langchain-chroma
langchain-huggingface

# Database
pymongo>=4.0
redis>=4.0

# ML & NLP
sentence-transformers
transformers

# Web & UI
streamlit>=1.20

# Utils
python-dotenv
```

---

## Configurazione

### Environment Variables

```bash
# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=rag_system
MONGO_USER=<optional>
MONGO_PASSWORD=<optional>

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<optional>
REDIS_DB=0

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest
```

### Directories

```
data/
├── vectorstores/          # ChromaDB collections
└── uploads/               # Temporary file uploads

docs/                      # User uploaded documents

chroma_db/                 # Legacy vector store
```

---

## Performance & Scalability

### Ottimizzazioni Implementate

1. **Chunking Efficiente**
   - Chunk size ottimizzato: 600 caratteri
   - Overlap: 200 caratteri (contesto)

2. **Caching**
   - Redis per chat history
   - Evita query ripetitive a MongoDB

3. **Similarity Threshold**
   - Filtraggio documenti poco rilevanti
   - Riduce context size per LLM

4. **Summarization**
   - Compressione storia conversazioni
   - Mantiene context window gestibile

### Limitazioni Attuali

- **Single LLM Instance**: Ollama locale (no load balancing)
- **No Horizontal Scaling**: Architettura single-process
- **Vector Store**: ChromaDB locale (non distribuito)

### Possibili Miglioramenti

1. **Scalabilità**
   - Deploy LLM su cluster
   - Vector DB distribuito (Pinecone, Weaviate)
   - Load balancer per Streamlit

2. **Performance**
   - Async processing per ingestion
   - Batch embeddings
   - Cache risultati query frequenti

3. **Monitoraggio**
   - Logging strutturato
   - Metrics (latency, usage)
   - Error tracking

---

## Testing

### Test Suite Structure

```
test/
└── unit/
    ├── agents/
    │   ├── test_router.py
    │   └── test_summarizer.py
    ├── ingestion/
    │   └── test_ingestion.py
    └── tools/
        └── test.py
```

### Evaluation Metrics

Il sistema include valutazione automatica con:
- **BLEU**: Similarità n-gram
- **ROUGE-L**: Longest common subsequence
- **F1 Score**: Precision & Recall
- **Semantic Similarity**: Cosine similarity embeddings

---

## Sicurezza

### Considerazioni

1. **Input Validation**: Validazione documenti caricati
2. **SQL/NoSQL Injection**: Parametrizzazione query
3. **Secrets Management**: Environment variables
4. **Rate Limiting**: Da implementare per produzione

### Best Practices

- Non committare credenziali in git
- Usare `.env` per configurazione locale
- Validare input utente prima di processing
- Limitare dimensione upload file

---

## Deployment

### Requirements

```bash
# System dependencies
- Python 3.10+
- MongoDB 5.0+
- Redis 6.0+
- Ollama (per LLM locale)

# Python packages
pip install -r requirements.txt
```

### Setup Locale

```bash
# 1. Start MongoDB
mongod --dbpath /path/to/data

# 2. Start Redis
redis-server

# 3. Start Ollama
ollama serve
ollama pull llama3

# 4. Start Application
streamlit run presentation/notebook_page.py
```

### Docker (Futuro)

Containerizzazione per deployment semplificato:
- Container per app Python
- Container MongoDB
- Container Redis
- Container Ollama

---

## Roadmap

### Features in Sviluppo

- [ ] Cancellazione selettiva documenti
- [ ] Gestione permessi utenti
- [ ] Export notebook (PDF, Markdown)
- [ ] Statistiche utilizzo

### Miglioramenti Tecnici

- [ ] Containerizzazione Docker
- [ ] CI/CD pipeline
- [ ] Monitoring e logging
- [ ] API REST per integrazione

---

## Contribuire

### Setup Ambiente Sviluppo

```bash
# Clone repo
git clone https://github.com/minicla03/Q-AmodelAI.git

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest test/
```

### Code Style

- PEP 8 per Python
- Docstrings per funzioni pubbliche
- Type hints dove possibile

---

## Contatti & Supporto

Per domande o supporto:
- **GitHub Issues**: [Q-AmodelAI Issues](https://github.com/minicla03/Q-AmodelAI/issues)
- **Maintainer**: minicla03

---

*Documento aggiornato: Novembre 2025*
