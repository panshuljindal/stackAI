from uuid import UUID
from typing import List
from app.repositories.library_repo import LibraryRepository
from app.schemas.search import SearchRequest, SearchResult
from app.models.chunk import Chunk
from app.indexing.manager import VectorIndexManager
from numpy import dot
from numpy.linalg import norm
import numpy as np

index_manager = VectorIndexManager()
class SearchController:
    def __init__(self, library_repo: LibraryRepository):
        self.library_repo = library_repo

    def search(self, request: SearchRequest) -> List[SearchResult]:
        library = self.library_repo.get_library(str(request.library_id))

        if not library:
            raise ValueError("Library not found")

        raw_results = index_manager.search(
            library_id=request.library_id,
            query_vector=request.query_embedding,
            top_k=request.top_k,
            filters=request.filters
        )

        results: List[SearchResult] = [
            SearchResult(
                chunk_id=chunk_id,
                document_id=None,
                text=metadata.get("text", ""),
                score=round(score, 4)
            )
            for chunk_id, score, metadata in raw_results
        ]

        return results

    def _apply_filters(self, chunks: List[tuple], request: SearchRequest) -> List[tuple]:
        if not request.filters:
            return chunks

        f = request.filters
        result = []
        for doc_id, chunk in chunks:
            if f.text_contains and f.text_contains.lower() not in chunk.text.lower():
                continue
            if f.created_after and chunk.created_at < f.created_after:
                continue
            if f.created_before and chunk.created_at > f.created_before:
                continue
            if f.metadata_key and f.metadata_value:
                if chunk.metadata.get(f.metadata_key) != f.metadata_value:
                    continue
            result.append((doc_id, chunk))
            
        return result
