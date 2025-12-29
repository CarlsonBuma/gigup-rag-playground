# ⏱️ **10‑Minute RAG Crash Course**  
### *Everything you need to understand RAG — fast.*

This crash course gives you the essential concepts, mental models, and workflows behind Retrieval‑Augmented Generation (RAG).  
If you read this once, you’ll understand 80% of how modern AI assistants, search engines, and knowledge systems work.

---

# 🧠 1. What Problem Does RAG Solve?

LLMs are powerful, but they have limitations:

- They **hallucinate**  
- They **don’t know your private data**  
- They **can’t stay up‑to‑date**  
- They **forget long documents**  
- They **can’t store large knowledgebases internally**

RAG fixes all of this by giving the model a **memory extension**.

---

# 🧠 What RAG Is — The Core Concept

**RAG = Retrieval‑Augmented Generation**

Think of it like this: Instead of asking an AI model to "remember everything," you give it the ability to look things up in a knowledgebase when needed.

### The Two Halves of RAG:

#### 1️⃣ **Retrieval** (Finding)
Search your knowledge base for the most relevant pieces of information related to a user's question.

#### 2️⃣ **Generation** (Answering)
Feed those retrieved pieces to an LLM to produce an accurate, grounded answer.

### Why RAG Works Better:
| Problem | How RAG Solves It |
|---------|-------------------|
| Hallucination | Answers are grounded in real documents |
| Outdated info | You control what's in the knowledge base |
| Black box | You see exactly what documents were retrieved |
| Privacy | Everything stays local on your machine |
| Accuracy | Answers cite sources from your documents |

---

# 🧩 3. The RAG Pipeline (Simple Version)

```
User Question
      ↓
Embed the question (vector)
      ↓
Search vector database (pgvector)
      ↓
Retrieve top‑k relevant chunks
      ↓
Feed chunks + question to LLM
      ↓
LLM generates grounded answer
```

That’s it.  
Everything else is just engineering around this loop.

---

# 📄 4. How Documents Become Searchable

Before retrieval can work, you must **prepare your documents**.

### Step 1 — Extract text  
From PDFs, HTML, Markdown, etc.

### Step 2 — Chunk text  
Split into small, meaningful pieces (e.g., 1000 characters).

### Step 3 — Embed each chunk  
Convert text → vector using a multilingual embedding model.

### Step 4 — Store in pgvector  
Each chunk becomes a row:

- text  
- embedding  
- document ID  
- chunk index  

Now your knowledgebase is ready.

---

# 🧠 5. What Are Embeddings?

Embeddings are **numerical fingerprints of meaning**.

Example:

- “developer”  
- “software engineer”  

→ Their vectors are close together.

Embeddings allow **semantic search**, not keyword search.

Your model:  
**mxbai‑embed‑large**  
- multilingual  
- 1024‑dimensional  
- perfect for resumes, documents, knowledgebases

---

# 🔍 6. How Vector Search Works

When a user asks a question:

1. Convert the question to an embedding  
2. Compare it to all stored embeddings  
3. Sort by **cosine distance**  
4. Return the closest matches  

This is how the system “understands” meaning.

---

# 🤖 7. Where the LLM Fits In

The LLM (e.g., `smollm:360m`) is **not** used for search.  
It is used **after** retrieval.

The LLM takes:

- the user question  
- the retrieved chunks  

…and produces a grounded answer.

This prevents hallucination because the model is forced to use real data.

---

# 🧱 8. Why Chunking Matters

Chunking is one of the most important parts of RAG.

- Too big → embeddings become noisy  
- Too small → lose context  
- Too random → retrieval becomes inaccurate  

Your chunker uses:

- `RecursiveCharacterTextSplitter`  
- chunk size: **1000**  
- overlap: **150**  

This is a modern, RAG‑friendly setup.

---

# 🧪 9. What Happens During a Search (Step‑by‑Step)

```
User: "What skills does the candidate have?"
```

1. Normalize + embed the query  
2. pgvector finds the closest chunks  
3. Return the top 3 chunks  
4. (Optional) LLM summarizes them  
5. User gets a grounded answer  

This is the entire RAG loop.

---

# 🧭 10. Mental Models for RAG

### ✔ RAG is not magic  
It’s structured search + structured generation.

### ✔ Embeddings are the heart of retrieval  
Good embeddings → good search.

### ✔ LLM is optional  
Retrieval alone is already powerful.

### ✔ Everything is local  
Your playground uses **no external APIs**.

### ✔ RAG is predictable  
You always know *why* the model answered the way it did —  
because you can inspect the retrieved chunks.

---

# 🎯 Final Takeaway

If you understand these 10 points, you understand RAG:

1. Extract text  
2. Chunk text  
3. Embed chunks  
4. Store vectors  
5. Embed query  
6. Vector search  
7. Retrieve top‑k  
8. Feed to LLM  
9. Generate grounded answer  
10. Repeat  

This is the foundation of modern AI search systems.
