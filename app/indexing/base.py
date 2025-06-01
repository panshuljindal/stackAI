from abc import ABC, abstractmethod
from typing import List, Tuple
from uuid import UUID

class VectorIndex(ABC):
    @abstractmethod
    def add(self, chunk_id: UUID, vector: List[float], metadata: dict): ...
    
    @abstractmethod
    def search(self, query_vector: List[float], top_k: int, filters: dict = None) -> List[Tuple[UUID, float, dict]]: ...
