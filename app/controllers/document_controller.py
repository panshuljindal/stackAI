from uuid import UUID
from typing import Dict
from app.models.document import Document
from app.models.chunk import Chunk
from app.repositories.library_repo import LibraryRepository

class DocumentController:
    def __init__(self, repo: LibraryRepository):
        self.repo = repo

    def add_document(self, library_id: UUID, document_data: Dict) -> Document:
        document = Document.create(
            name=document_data["name"],
            metadata=document_data.get("metadata", {}),
            chunks=[]
        )
        self.repo.add_document(library_id, document)
        return document

    def get_document(self, library_id: UUID, document_id: UUID) -> Document:
        return self.repo.get_document(library_id, document_id)

    def add_chunk(self, library_id: UUID, document_id: UUID, chunk_data: Dict) -> Chunk:
        chunk = Chunk.create(
            text = chunk_data["text"],
            embedding = chunk_data["embedding"], # Can add logic to handle embedding generation usig cohere API
            metadata = chunk_data.get("metadata", {})
        )
        self.repo.add_chunk(library_id, document_id, chunk)
        return chunk
    
    def delete_chunk(self, library_id: UUID, document_id: UUID, chunk_id: UUID):
        library = self.library_repo.get(str(library_id))
        if not library:
            raise ValueError("Library not found")

        document = next((doc for doc in library.documents if doc.id == document_id), None)
        if not document:
            raise ValueError("Document not found")

        chunk_index = next((i for i, ch in enumerate(document.chunks) if ch.id == chunk_id), None)
        if chunk_index is None:
            raise ValueError("Chunk not found")

        del document.chunks[chunk_index]
        self.library_repo.save_to_disk()
