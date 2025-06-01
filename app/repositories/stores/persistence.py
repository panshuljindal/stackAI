import os
import json
from threading import RLock
from uuid import UUID
from datetime import datetime
from typing import Dict, List
from pydantic.json import pydantic_encoder
from app.models.library import Library
from app.models.document import Document
from app.models.chunk import Chunk

class PersistenceStore:
    def __init__(self, store: Dict[str, Library], lock: RLock, storage_file: str):
        self.store = store
        self.lock = lock
        self.storage_file = storage_file

    def save(self):
        with self.lock:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            with open(self.storage_file, "w") as f:
                json.dump({k: v.dict() for k, v in self.store.items()}, f, default=pydantic_encoder, indent=2)

    def load(self):
        if not os.path.exists(self.storage_file):
            return

        with open(self.storage_file, "r") as f:
            try:
                raw_data = json.load(f)
            except json.JSONDecodeError:
                print(f"[WARN] Corrupted JSON in {self.storage_file}.")
                return

        with self.lock:
            self.store.clear()
            for lib_id, lib_dict in raw_data.items():
                documents: List[Document] = []
                for doc_dict in lib_dict["documents"]:
                    chunks: List[Chunk] = [
                        Chunk(**chunk_dict) for chunk_dict in doc_dict["chunks"]
                    ]
                    documents.append(Document(
                        id=UUID(doc_dict["id"]),
                        name=doc_dict["name"],
                        metadata=doc_dict["metadata"],
                        chunks=chunks,
                        created_at=datetime.fromisoformat(doc_dict["created_at"])
                    ))

                self.store[lib_id] = Library(
                    id=UUID(lib_dict["id"]),
                    name=lib_dict["name"],
                    metadata=lib_dict["metadata"],
                    documents=documents,
                    created_at=datetime.fromisoformat(lib_dict["created_at"])
                )
