from pydantic import BaseModel
from typing import Dict, List
from uuid import UUID, uuid4
from datetime import datetime
from app.models.document import Document

class Library(BaseModel):
    id: UUID
    name: str
    metadata: Dict[str, str]
    documents: List[Document]
    created_at: datetime

    @staticmethod
    def create(name: str, metadata: Dict[str, str]) -> "Library":
        return Library(
            id=uuid4(),
            name=name,
            metadata=metadata,
            documents=[],
            created_at=datetime.utcnow()
        )