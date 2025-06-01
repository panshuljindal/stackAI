from pydantic import BaseModel
from typing import Dict, List
from uuid import UUID, uuid4
from datetime import datetime
from app.models.chunk import Chunk

class Document(BaseModel):
    id: UUID
    name: str
    metadata: Dict[str, str]
    chunks: List[Chunk]
    created_at: datetime

    @staticmethod
    def create(name: str, metadata: Dict[str, str], chunks: List[Chunk]) -> "Document":
        return Document(
            id=uuid4(),
            name=name,
            metadata=metadata,
            chunks=chunks,
            created_at=datetime.utcnow()
        )