from pydantic import BaseModel, Field
from typing import List, Dict
from uuid import UUID
class ChunkCreate(BaseModel):
    text: str
    library_id: UUID
    document_id: UUID
    embedding: List[float]
    metadata: Dict[str, str] = Field(default_factory=dict)

class ChunkResponse(BaseModel):
    id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, str]
    created_at: str