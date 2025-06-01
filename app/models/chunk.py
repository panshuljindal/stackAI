from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID, uuid4
from datetime import datetime

class Chunk(BaseModel):
    id: UUID
    text: str
    embedding: List[float]
    metadata: Dict[str, str]
    created_at: datetime

    @staticmethod
    def create(text: str, embedding: List[float], metadata: Dict[str, str]) -> "Chunk":
        return Chunk(
            id=uuid4(),
            text=text,
            embedding=embedding,
            metadata=metadata,
            created_at=datetime.utcnow()
        )