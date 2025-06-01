from uuid import UUID
from threading import RLock
from typing import Dict
from app.models.library import Library
from app.models.chunk import Chunk

class ChunkStore:
    def __init__(self, store: Dict[str, Library], lock: RLock):
        self.store = store
        self.lock = lock

    def add(self, library_id: UUID, document_id: UUID, chunk: Chunk):
        with self.lock:
            library = self.store.get(str(library_id))
            if not library:
                raise ValueError("Library not found")

            document = next((doc for doc in library.documents if doc.id == document_id), None)
            if not document:
                raise ValueError("Document not found in library")

            document.chunks.append(chunk)
