from uuid import UUID
from typing import List
from app.repositories.library_repo import LibraryRepository
from app.schemas.search import SearchRequest, SearchResult
from app.models.chunk import Chunk
from numpy import dot
from numpy.linalg import norm
import numpy as np


class SearchController:
    def __init__(self, library_repo: LibraryRepository):
        self.library_repo = library_repo

    def search(self, request: SearchRequest) -> List[SearchResult]:
        library = self.library_repo.get(str(request.library_id))

        if not library:
            raise ValueError("Library not found")

        all_chunks: List[Chunk] = []

        for doc in library.documents:
            for chunk in doc.chunks:
                all_chunks.append((doc.id, chunk))

        filtered = self._apply_filters(all_chunks, request)

        results = []
        query_vec = np.array(request.query_embedding)

        for doc_id, chunk in filtered:
            chunk_vec = np.array(chunk.embedding)
            if norm(chunk_vec) == 0 or norm(query_vec) == 0:
                continue
            score = dot(query_vec, chunk_vec) / (norm(query_vec) * norm(chunk_vec))
            results.append(SearchResult(
                chunk_id=chunk.id,
                document_id=doc_id,
                text=chunk.text,
                score=round(float(score), 4)
            ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:request.top_k]

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
