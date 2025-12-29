from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector
from core.database import Base
from core.config import Config

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(int(Config.DB_VECTOR_DIMENSION)))
    token_count = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationship back to Document
    document = relationship(
        "Document",
        back_populates="chunks"
    )
