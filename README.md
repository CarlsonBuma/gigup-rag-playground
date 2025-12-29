# Local RAG Playground — A Microlearning Guide

Welcome to the Local RAG Playground — a hands‑on environment designed to help you understand how Retrieval‑Augmented Generation (RAG) works using Python, Ollama, and pgvector.

This project is intentionally simple, transparent, and educational.
Everything runs locally, so you can explore RAG concepts without external APIs or cloud dependencies.

## 🧩 What This Project Is

This project is a lightweight, fully local Retrieval‑Augmented Generation (RAG) system built with:

- **Python** — Core language
- **Ollama** — Local LLM + Embeddings engine
- **PostgreSQL + pgvector** — Vector database
- **LangChain** — Text splitting & orchestration
- **Jupyter** — Interactive experimentation notebooks

### You Can:
- Ingest documents (PDFs, resumes, knowledge files)
- Chunk them into semantically meaningful pieces
- Embed them using multilingual embedding models
- Store embeddings in a vector database
- Perform semantic search over your knowledgebase
- Generate answers grounded in your documents

## 🚀 Features

| Feature | Benefit |
|---------|---------|
| 📄 PDF ingestion with text extraction | Easy document loading |
| ✂️ Semantic chunking | Preserves context & meaning |
| 🧠 Multilingual embeddings | Works across languages |
| 🔍 Vector similarity search | Find relevant content fast |
| 🧱 Modular architecture | Easy to understand & extend |
| 🧪 Jupyter notebooks | Learn interactively |
| 🔒 Fully local | No external APIs, complete privacy |


## 🧱 Architecture Overview

### The RAG Pipeline

```
Ingestion Phase:
  PDF → PdfChunker → Semantic Chunks
                           ↓
                    Embedding (Ollama)
                           ↓
                     pgvector (Store)

Retrieval Phase:
  User Query → Embedding (Ollama) → Vector Search → Top K Chunks → LLM → Answer
```

### Data Flow Example:

```
1. Upload file.pdf
   └─ Extract text
   └─ Split into chunks (preserving context)
   └─ Convert each chunk to embedding vector
   └─ Store in PostgreSQL with pgvector

2. User asks: "What are the candidate's skills?"
   └─ Convert question to embedding
   └─ Search pgvector for similar chunks (cosine distance)
   └─ Retrieve top 3 matching chunks
   └─ Pass to LLM: "Based on these chunks, answer the question"
   └─ Return grounded answer
```

## 🧩 Core Components

| Component | Purpose |
|-----------|---------|
| **Ollama** | Provides embeddings + LLM generation locally |
| **PdfChunker** | Extracts text from PDFs, intelligently chunks content |
| **Embedding Engine** | Converts text to 1024-dim vectors |
| **PostgreSQL + pgvector** | Stores vectors, performs similarity search |
| **RagController** | Orchestrates ingestion, search, generation |
| **SQLAlchemy Models** | ORM for documents, chunks, embeddings |

Each component is intentionally small and easy to understand.

## ⚙️ System Requirements

### Hardware

- **RAM**: 8 GB minimum (16 GB recommended for smooth operation)
- **Disk**: 10 GB+ for models and data
- **CPU**: Modern processor (LLMs work on CPU, but benefit from adequate cores)

### Software

- **Python 3.10+**
- **PostgreSQL 13+** with pgvector extension
  - Vector column: `embedding vector(1024)`
- **Ollama** installed and running locally
- **Docker** (optional, for containerized services)
