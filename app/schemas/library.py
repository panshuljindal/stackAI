from pydantic import BaseModel, Field
from typing import List, Dict
from app.schemas.document import DocumentResponse

class LibraryCreate(BaseModel):
    name: str
    metadata: Dict[str, str] = Field(default_factory=dict)

class LibraryResponse(BaseModel):
    id: str
    name: str
    metadata: Dict[str, str]
    documents: List[DocumentResponse]
    created_at: str