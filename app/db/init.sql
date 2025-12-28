-- 1. Documents (original sources)
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    source_type TEXT, -- pdf, html, text, survey, etc.
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Chunks (RAG core)
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(960), -- adjust depending on model
    token_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast vector search
CREATE INDEX idx_chunks_document_id ON chunks(document_id);
CREATE INDEX idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops);
