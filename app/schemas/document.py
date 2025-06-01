from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Dict
from app.schemas.chunk import ChunkCreate, ChunkResponse

class DocumentCreate(BaseModel):
    library_id: UUID 
    name: str
    metadata: Dict[str, str] = Field(default_factory=dict)
    chunks: List[ChunkCreate] = Field(default_factory=list)

class DocumentResponse(BaseModel):
    id: str
    name: str
    metadata: Dict[str, str]
    chunks: List[ChunkResponse]
    created_at: str