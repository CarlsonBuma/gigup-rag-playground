from sqlalchemy import select
from core.config import Config
from models.document import Document
from models.document_chunk import DocumentChunk


class RagIngestionController:
    def __init__(self, db, ollama, chunker):
        self.db = db
        self.ollama = ollama
        self.chunker = chunker

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

    def add_chunk(self, document_id, chunk_index, content):
        embedding = self.ollama.embed(content)

        if embedding is None:
            raise ValueError(
                f"❌ Embedding failed for chunk {chunk_index}. "
                f"Check OLLAMA_EMBEDDING_MODEL and Ollama server logs."
            )

        expected_dim = Config.DB_VECTOR_DIMENSION
        if len(embedding) != expected_dim:
            raise ValueError(
                f"❌ Embedding dimension mismatch: got {len(embedding)}, "
                f"expected {expected_dim}."
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
