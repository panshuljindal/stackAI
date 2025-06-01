from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class SearchFilters(BaseModel):
    text_contains: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    metadata_key: Optional[str] = None
    metadata_value: Optional[str] = None

class SearchRequest(BaseModel):
    library_id: UUID
    query_embedding: List[float]
    top_k: int = Field(..., gt=0, le=100)
    filters: Optional[SearchFilters] = None

class SearchResult(BaseModel):
    chunk_id: UUID
    document_id: UUID
    text: str
    score: float
