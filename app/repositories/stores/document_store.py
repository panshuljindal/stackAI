from uuid import UUID
from threading import RLock
from typing import Dict
from app.models.library import Library
from app.models.document import Document

class DocumentStore:
    def __init__(self, store: Dict[str, Library], lock: RLock):
        self.store = store
        self.lock = lock

    def add(self, library_id: UUID, document: Document):
        with self.lock:
            library = self.store.get(str(library_id))
            if not library:
                raise ValueError("Library not found")

            if any(doc.id == document.id for doc in library.documents):
                raise ValueError("Document with this ID already exists in the library")

            library.documents.append(document)

    def get(self, library_id: UUID, document_id: UUID) -> Document:
        with self.lock:
            library = self.store.get(str(library_id))
            if not library:
                raise ValueError("Library not found")

            for doc in library.documents:
                if doc.id == document_id:
                    return doc

            raise ValueError("Document not found in library")
