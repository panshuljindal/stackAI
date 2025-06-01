from uuid import UUID
from typing import Dict
from threading import RLock
from app.models.library import Library

class LibraryStore:
    def __init__(self, store: Dict[str, Library], lock: RLock):
        self.store = store
        self.lock = lock

    def get(self, library_id: UUID) -> Library:
        with self.lock:
            library = self.store.get(str(library_id))
            if not library:
                raise ValueError("Library not found")
            return library

    def add(self, library: Library):
        with self.lock:
            key = str(library.id)
            if key in self.store:
                raise ValueError("Library with this ID already exists")
            self.store[key] = library

    def delete(self, library_id: UUID):
        with self.lock:
            key = str(library_id)
            if key not in self.store:
                raise ValueError("Library not found")
            del self.store[key]

    def list(self) -> Dict[str, Library]:
        with self.lock:
            return dict(self.store)
