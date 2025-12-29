from sqlalchemy import select
from sqlalchemy.sql import func
from core.database import Database
from core.ollama import Ollama
from core.config import Config
from models.document import Document
from models.document_chunk import DocumentChunk
from .modules.PdfChunker import PdfChunker


class RagController:
    def __init__(self):
        self.db = Database()
        self.ollama = Ollama()  # Uses OLLAMA_EMBEDDING_MODEL from .env
        self.chunker = PdfChunker()

    def _embed(self, text: str):
        return self.ollama.embed(text)
    
    def _expand_query(self, query: str) -> str:
        return (
            query
            + " skills experience responsibilities achievements projects education certifications tools roles job titles"
        )

    # -----------------------------
    # SEARCH: Vector Similarity (Cosine)
    # -----------------------------
    def search(self, query: str, limit: int = 3):
        # Normalize + expand
        query = query.strip().lower()
        expanded = self._expand_query(query)

        qvec = self._embed(expanded)

        session = self.db.session()
        try:
            stmt = (
                select(
                    DocumentChunk.id,
                    DocumentChunk.document_id,
                    DocumentChunk.chunk_index,
                    DocumentChunk.content,
                    DocumentChunk.embedding.cosine_distance(qvec).label("distance")
                )
                .order_by("distance")
                .limit(limit * 5)  # fetch more candidates
            )

            rows = session.execute(stmt).all()

            # keep only top-k
            rows = rows[:limit]

            return [
                {
                    "id": r.id,
                    "document_id": r.document_id,
                    "chunk_index": r.chunk_index,
                    "content": r.content,
                    "distance": float(r.distance),
                }
                for r in rows
            ]

        finally:
            session.close()

            
    # -----------------------------
    # GET ALL: Chunks in DB
    # -----------------------------
    def get_chunks(self):
        session = self.db.session()
        try:
            stmt = (
                select(DocumentChunk)
                .order_by(
                    DocumentChunk.document_id.asc(),
                    DocumentChunk.chunk_index.asc()
                )
            )
            return session.execute(stmt).scalars().all()
        finally:
            session.close()

    # -----------------------------
    # CREATE: PDF → Chunks → DB
    # -----------------------------
    def chunk_pdf(self, pdf_path: str):
        chunks = self.chunker.process_pdf(pdf_path)

        doc = self.add_document(
            title=pdf_path,
            description="PDF document",
            source_type="pdf"
        )

        for idx, chunk in enumerate(chunks):
            self.add_chunk(doc.id, idx, chunk)

        return chunks


    # -----------------------------
    # ORM: Add Document
    # -----------------------------
    def add_document(self, title, description=None, source_type=None):
        session = self.db.session()
        try:
            doc = Document(
                title=title,
                description=description,
                source_type=source_type
            )
            session.add(doc)
            session.commit()
            session.refresh(doc)
            return doc
        finally:
            session.close()


    # -----------------------------
    # ORM: Add Chunk (Improved)
    # -----------------------------
    def add_chunk(self, document_id, chunk_index, content):
        embedding = self._embed(content)

        # -----------------------------
        # VALIDATION: Embedding must exist
        # -----------------------------
        if embedding is None:
            raise ValueError(
                f"❌ Embedding failed for chunk {chunk_index}. "
                f"Check OLLAMA_EMBEDDING_MODEL and Ollama server logs."
            )

        # -----------------------------
        # VALIDATION: Embedding dimension must match DB
        # -----------------------------
        expected_dim = Config.DB_VECTOR_DIMENSION
        if len(embedding) != expected_dim:
            raise ValueError(
                f"❌ Embedding dimension mismatch: got {len(embedding)}, "
                f"expected {expected_dim}. "
                f"Check your .env and pgvector schema."
            )

        token_count = len(content.split())

        session = self.db.session()
        try:
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk_index,
                content=content,
                embedding=embedding,
                token_count=token_count
            )
            session.add(chunk)
            session.commit()
        finally:
            session.close()
