from uuid import UUID
from typing import List, Dict
from app.models.library import Library
from app.models.document import Document
from app.models.chunk import Chunk
from app.repositories.library_repo import LibraryRepository

class LibraryController:
    def __init__(self, repo: LibraryRepository):
        self.repo = repo

    def create_library(self, name: str, metadata: Dict[str, str]) -> Library:
        library = Library.create(name=name, metadata=metadata)
        self.repo.create_library(library)
        return library

    def get_library(self, library_id: UUID) -> Library:
        return self.repo.get_library(library_id)

    def delete_library(self, library_id: UUID):
        self.repo.delete_library(library_id)

    def list_libraries(self) -> List[Library]:
        return list(self.repo.list_libraries().values())

    def update_library(self, library_id: UUID, name: str, metadata: Dict[str, str]) -> Library:
        library = self.repo.get_library(library_id)
        if not library:
            raise ValueError("Library not found")
        
        library.name = name
        library.metadata = metadata
        self.repo.update_library(library)
        return library