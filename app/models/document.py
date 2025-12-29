from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    source_type = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationship to chunks
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete"
    )
