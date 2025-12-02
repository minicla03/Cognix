# Cognix: A Multilingual PDF-Based Question-Answering System

## 1. Introduction

Cognix is an intelligent document-based question-answering (QA) system designed to help users interact with their personal PDF documents through natural language queries. The system leverages Retrieval-Augmented Generation (RAG) architecture to provide accurate, context-aware responses based on user-uploaded content.

In today's information-rich environment, users often struggle to efficiently extract relevant information from large document collections. Traditional keyword-based search methods fall short when users seek conceptual understanding or specific explanations from technical documents. Cognix addresses this challenge by combining the power of modern Large Language Models (LLMs) with semantic document retrieval, enabling users to ask questions in natural language and receive comprehensive, source-backed answers.

The system distinguishes itself through its robust multilingual support, handling queries in Italian, English, Spanish, French, and German. This multilingual capability makes Cognix particularly valuable for international academic and professional contexts where documents and users may operate across different languages. Beyond simple question-answering, Cognix extends its functionality to include automatic generation of flashcards and quizzes, supporting active learning methodologies and knowledge retention.

This report presents the design, implementation, and evaluation of Cognix, demonstrating its effectiveness as a learning companion and document exploration tool.

---

## 2. Aims and Objectives

The primary aim of this project is to develop an intelligent, multilingual document-based QA system that enables efficient knowledge extraction from PDF documents. The specific objectives are:

1. **Document Ingestion and Processing**
   - Implement robust PDF parsing and text extraction capabilities
   - Support multiple document formats (PDF, DOCX, TXT, HTML, CSV)
   - Develop efficient text chunking strategies for optimal retrieval

2. **Semantic Search Implementation**
   - Integrate multilingual embedding models for cross-language semantic similarity
   - Implement vector database storage using Chroma for persistent document indexing
   - Develop configurable retrieval mechanisms with similarity thresholds

3. **Intelligent Tool Routing**
   - Create an LLM-based routing agent to classify user intent
   - Support three distinct tools: QA, Flashcard generation, and Quiz generation
   - Handle multilingual queries with accurate intent detection

4. **Multilingual Response Generation**
   - Support five languages: Italian, English, Spanish, French, and German
   - Implement automatic language detection from user queries
   - Generate responses in the user's preferred language

5. **Educational Content Generation**
   - Develop flashcard generation from document content
   - Implement quiz generation with multiple-choice questions
   - Support configurable difficulty levels and question counts

6. **System Evaluation and Quality Assurance**
   - Implement comprehensive evaluation frameworks for all system components
   - Measure QA quality using standard NLP metrics (BLEU, ROUGE, F1)
   - Evaluate routing accuracy across multilingual test cases

---

## 3. Background and Literature Review

### Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation, introduced by Lewis et al. (2020), combines the generative capabilities of large language models with external knowledge retrieval. This approach addresses a fundamental limitation of pure LLMs: their knowledge is fixed at training time and may become outdated or lack domain-specific information. RAG systems retrieve relevant documents from a knowledge base and provide them as context to the generative model, enabling more accurate and verifiable responses.

### Large Language Models for Question Answering

Modern LLMs such as GPT-4, LLaMA, and DeepSeek have demonstrated remarkable capabilities in understanding and generating natural language. When applied to QA tasks, these models can comprehend complex questions, synthesize information from provided contexts, and generate coherent, human-like responses. The integration of LLMs with RAG architectures has become a standard approach for building domain-specific QA systems (Gao et al., 2023).

### Multilingual NLP and Embeddings

Cross-lingual understanding has been significantly advanced by multilingual embedding models such as mBERT and multilingual sentence transformers. The paraphrase-multilingual-MiniLM-L12-v2 model used in Cognix enables semantic similarity computation across different languages, allowing users to query documents regardless of the language mismatch between query and content.

### Document Processing and Chunking

Effective document chunking is crucial for RAG systems. Research by Liu et al. (2023) highlights the importance of chunk size and overlap in preserving context while maintaining retrieval precision. Recursive text splitting strategies, as implemented in LangChain, balance these considerations by intelligently segmenting documents at natural boundaries.

### Evaluation of QA Systems

Evaluating QA systems requires multiple metrics to capture different quality dimensions. Standard metrics include BLEU and ROUGE for measuring n-gram overlap with reference answers, and semantic similarity measures for capturing meaning preservation. The DeepEval framework provides comprehensive LLM-as-judge evaluation capabilities, including faithfulness, answer relevancy, and contextual metrics (Kryscinski et al., 2019).

---

## 4. Methodology

### System Architecture

Cognix follows a modular architecture organized into four main layers:

**1. Presentation Layer**
The user interface is built using a notebook-style GUI that allows users to upload PDF documents, manage their document collection, and interact with the system through natural language queries. The interface displays responses along with source document references for transparency.

**2. Ingestion Layer**
The document ingestion pipeline handles:
- Document loading using format-specific strategies (PDF, DOCX, TXT, HTML, CSV)
- Text splitting using RecursiveCharacterTextSplitter with 600-character chunks and 200-character overlap
- Embedding generation using the paraphrase-multilingual-MiniLM-L12-v2 model
- Vector storage in ChromaDB with persistent storage per notebook

**3. RAG Logic Layer**
The core intelligence of the system comprises:
- **Routing Agent**: An LLM-based classifier that analyzes user intent and routes queries to the appropriate tool (QA, Flashcard, or Quiz)
- **QA Tool**: Retrieves relevant document chunks and generates comprehensive answers
- **Flashcard Tool**: Creates question-answer pairs for study purposes
- **Quiz Tool**: Generates multiple-choice questions with configurable difficulty

**4. LLM Integration Layer**
A thread-safe singleton manages LLM interactions, supporting:
- OpenRouter API integration for model access
- DeepSeek-v3.1 as the primary model for response generation
- Configurable parameters including temperature, top-p, and context window size

### Language Detection and Multilingual Support

The system implements automatic language detection through pattern matching against known language indicators in queries. When explicit language hints are detected (e.g., "rispondi in italiano", "answer in English"), the system adapts its response accordingly. The multilingual embedding model ensures consistent semantic search quality across all supported languages.

### Evaluation Methodology

The evaluation framework assesses three main components:

1. **Router Evaluation**: Tests intent classification accuracy across 51 test cases with both standard and complex/ambiguous queries

2. **QA Evaluation**: Measures response quality using:
   - DeepEval metrics: Answer Relevancy, Contextual Precision, Contextual Recall, Faithfulness
   - Custom metrics: F1 Score, BLEU, ROUGE-L

3. **Summary Evaluation**: Assesses summarization quality through fluency, coherence, consistency, and entity density metrics

---

## 5. Results and Evaluation

### 5.1 Router Agent Performance

The routing agent was evaluated on a comprehensive test set of 51 queries, tested with both standard JSON format and TOON format inputs, resulting in 102 total test cases.

**Overall Results:**
| Metric | Value |
|--------|-------|
| Total Tests | 102 |
| Total Successes | 55 |
| Overall Success Rate | 53.92% |

**Performance by Tool:**
| Tool | Total Tests | Successes | Success Rate |
|------|-------------|-----------|--------------|
| QA_TOOL | 34 | 34 | 100.00% |
| FLASHCARD_TOOL | 36 | 14 | 38.89% |
| QUIZ_TOOL | 32 | 7 | 21.88% |

**Analysis:**
The QA_TOOL demonstrates perfect classification accuracy, indicating that the routing agent reliably identifies informational queries. However, the FLASHCARD_TOOL and QUIZ_TOOL show lower accuracy, particularly in handling:
- Ambiguous queries with mixed intents
- Colloquial or informal language
- Cross-language queries with typos
- Implicit tool requests without explicit keywords

The test set includes challenging cases such as:
- Mixed-language queries: "Explícame in English sobre TCP/IP, please"
- Minimal input: "Flashcards?", "Quiz!"
- Typos: "Fashcards sobre AI plz", "Qwiz about networking"
- Complex multi-intent requests

### 5.2 QA Tool Performance

The QA tool was evaluated across 24 multilingual test cases covering topics in Android development, software engineering, data analytics, and electronics measurement.

**Languages Tested:**
- Italian: 6 test cases
- English: 2 test cases
- Spanish: 2 test cases
- French: 2 test cases
- German: 12 test cases

**Evaluation Metrics:**

*DeepEval Metrics (LLM-as-Judge):*
- Answer Relevancy: Measures how well the generated answer addresses the question
- Contextual Precision: Evaluates the relevance of retrieved documents
- Contextual Recall: Measures coverage of relevant information from context
- Faithfulness: Assesses factual consistency with retrieved documents

*Custom Metrics:*
| Metric | Description |
|--------|-------------|
| F1 Score | Token-level precision and recall using multilingual BERT tokenization |
| BLEU | N-gram precision with smoothing for shorter responses |
| ROUGE-L | Longest common subsequence overlap for fluency assessment |

**Configuration Testing:**
The evaluation compared two configurations:
1. Standard JSON message format
2. TOON format encoding for potentially more efficient prompt handling

### 5.3 Summarization Quality

The summarization component was evaluated using four key dimensions following Kryscinski et al. (2019):

| Dimension | Description | Implementation |
|-----------|-------------|----------------|
| Fluency | Grammatical correctness and readability | DeepEval SummarizationMetric |
| Coherence | Structural organization and flow | Cosine similarity between adjacent sentence embeddings |
| Consistency | Factual alignment with source | LLM-based comparison scoring |
| Relevance | Inclusion of important information | Vagueness detection via LLM judgment |

**Additional Metrics:**
- Entity Density: Ratio of named entities to total tokens, indicating information richness
- Repetitiveness: Detection of unnecessary redundant information

### 5.4 System Configuration

The LLM was configured with the following hyperparameters:
| Parameter | Value |
|-----------|-------|
| Model | deepseek/deepseek-chat-v3.1 |
| Temperature | 0.1 |
| Top-p | 0.9 |
| Context Window | 4096 tokens |
| Max Tokens | 300 |
| Repeat Penalty | 1.1 |

**Embedding Configuration:**
- Model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- Chunk Size: 600 characters
- Chunk Overlap: 200 characters
- Similarity Threshold: 0.75
- Top-k Retrieval: 10 documents (filtered to 3 max)

---

## 6. Conclusion

This report presented Cognix, a multilingual document-based QA system that successfully combines RAG architecture with modern LLMs to enable efficient knowledge extraction from PDF documents. The system achieves its primary objectives of supporting multilingual queries, generating educational content, and providing source-backed responses.

**Key Achievements:**
1. Robust multilingual support across five languages with automatic language detection
2. Modular architecture enabling easy extension and maintenance
3. Comprehensive evaluation framework covering all major system components
4. Perfect routing accuracy for QA queries (100%) with room for improvement in tool-specific routing

**Limitations and Future Work:**
1. Router accuracy for Flashcard and Quiz tools requires improvement, potentially through fine-tuning or enhanced few-shot prompting
2. The system currently lacks conversation memory across sessions
3. Real-time document updates and incremental indexing could enhance user experience
4. Integration of multimodal capabilities (images, tables) would extend document coverage

**Future Directions:**
- Implement conversation summarization for long-term memory
- Develop user feedback mechanisms for continuous improvement
- Explore fine-tuning approaches for improved routing accuracy
- Add support for additional document formats and multimedia content

Cognix demonstrates the viability of RAG-based systems for educational and professional document exploration, providing a foundation for future development in intelligent document interaction tools.

---

## 7. References

1. Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., ... & Wang, H. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. *arXiv preprint arXiv:2312.10997*.

2. Kryscinski, W., Keskar, N. S., McCann, B., Xiong, C., & Socher, R. (2019). Neural Text Summarization: A Critical Evaluation. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP)*.

3. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474.

4. Liu, N., Zhang, S., Zhang, K., Zhang, C., Li, T., & Liu, Y. (2023). LLM Augmented LLMs: Expanding Capabilities through Composition. *arXiv preprint arXiv:2401.02412*.

5. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP)*.

6. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is All You Need. *Advances in Neural Information Processing Systems*, 30.

7. LangChain Documentation. (2024). *LangChain: Building applications with LLMs through composability*. Retrieved from https://python.langchain.com/

8. ChromaDB Documentation. (2024). *Chroma: The AI-native open-source embedding database*. Retrieved from https://www.trychroma.com/

9. DeepEval Documentation. (2024). *DeepEval: The Open-Source LLM Evaluation Framework*. Retrieved from https://docs.confident-ai.com/

10. Sentence Transformers Documentation. (2024). *Sentence-Transformers: Multilingual Sentence Embeddings*. Retrieved from https://www.sbert.net/
