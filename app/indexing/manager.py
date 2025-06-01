from uuid import UUID
from typing import Dict, List, Tuple
from app.indexing.brute_force import BruteForceIndex

class VectorIndexManager:
    def __init__(self):
        self.indexes: Dict[UUID, BruteForceIndex] = {}

    def get_or_create_index(self, library_id: UUID) -> BruteForceIndex:
        if library_id not in self.indexes:
            self.indexes[library_id] = BruteForceIndex()
        return self.indexes[library_id]

    def add(self, library_id: UUID, chunk_id: UUID, vector: List[float], metadata: dict):
        self.get_or_create_index(library_id).add(chunk_id, vector, metadata)

    def search(self, library_id: UUID, query_vector: List[float], top_k: int, filters: dict = None):
        index = self.get_or_create_index(library_id)
        return index.search(query_vector, top_k, filters)
