from sqlalchemy import select
from models.document_chunk import DocumentChunk


class RagRetrievalController:
    def __init__(self, db, ollama):
        self.db = db
        self.ollama = ollama

    def _expand_query(self, query: str) -> str:
        return (
            query
            + " skills experience responsibilities achievements projects "
              "education certifications tools roles job titles"
        )

    def search(self, query: str, limit: int = 3):
        query = query.strip().lower()
        expanded = self._expand_query(query)

        qvec = self.ollama.embed(expanded)

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
                .limit(limit * 5)
            )

            rows = session.execute(stmt).all()
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
