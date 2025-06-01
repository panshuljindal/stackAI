from uuid import UUID
from threading import RLock
from typing import Dict
from app.models.library import Library
from app.models.document import Document
from app.models.chunk import Chunk
from app.utils.constants import LIBRARY_STORAGE_FILE
from app.repositories.stores.library_store import LibraryStore
from app.repositories.stores.document_store import DocumentStore
from app.repositories.stores.chunk_store import ChunkStore
from app.repositories.stores.persistence import PersistenceStore

class LibraryRepository:
    def __init__(self, storage_file: str = LIBRARY_STORAGE_FILE):
        
        self._store: Dict[str, Library] = {}
        self._lock = RLock()
        self._storage_file = storage_file

        self._library_store = LibraryStore(self._store, self._lock)
        self._document_store = DocumentStore(self._store, self._lock)
        self._chunk_store = ChunkStore(self._store, self._lock)
        self._persistence = PersistenceStore(self._store, self._lock, self._storage_file)

        self._persistence.load()

    # ------------------- Library Operations -------------------
    def create_library(self, library: Library):
        self._library_store.add(library)
        self.save()

    def get_library(self, library_id: UUID) -> Library:
        return self._library_store.get(library_id)

    def delete_library(self, library_id: UUID):
        self._library_store.delete(library_id)
        self.save()

    def list_libraries(self) -> Dict[str, Library]:
        return self._library_store.list()

    # ------------------- Document Operations -------------------
    def add_document(self, library_id: UUID, document: Document):
        self._document_store.add(library_id, document)
        self.save()

    def get_document(self, library_id: UUID, document_id: UUID) -> Document:
        return self._document_store.get(library_id, document_id)

    # ------------------- Chunk Operations -------------------
    def add_chunk(self, library_id: UUID, document_id: UUID, chunk: Chunk):
        self._chunk_store.add(library_id, document_id, chunk)
        self.save()

    def save(self):
        self._persistence.save()
