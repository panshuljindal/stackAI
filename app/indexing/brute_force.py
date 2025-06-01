import numpy as np
from typing import List, Tuple
from uuid import UUID
from app.indexing.base import VectorIndex

class BruteForceIndex(VectorIndex):
    def __init__(self):
        self.vectors = []

    def add(self, chunk_id: UUID, vector: List[float], metadata: dict):
        self.vectors.append((chunk_id, np.array(vector), metadata))

    def search(self, query_vector: List[float], top_k: int, filters: dict = None) -> List[Tuple[UUID, float, dict]]:
        query = np.array(query_vector)
        scored = []

        for chunk_id, vec, meta in self.vectors:
            if self._passes_filters(meta, filters):
                similarity = self._cosine_similarity(query, vec)
                scored.append((chunk_id, similarity, meta))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _passes_filters(self, metadata: dict, filters: dict) -> bool:
        if not filters:
            return True
        for key, value in filters.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True
