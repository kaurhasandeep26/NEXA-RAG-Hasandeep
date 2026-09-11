"""Persistent local ChromaDB storage."""
from __future__ import annotations

from typing import Any

import chromadb


class VectorStore:
    COLLECTION = "nexa_knowledge"

    def __init__(self, persist_path: str) -> None:
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION, metadata={"hnsw:space": "cosine"}
        )

    def document_exists(self, document_hash: str) -> bool:
        return bool(self.collection.get(where={"document_hash": document_hash}, limit=1)["ids"])

    def add_chunks(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict[str, Any]]) -> None:
        self.collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    def query(self, embedding: list[float], top_k: int) -> list[dict[str, Any]]:
        if self.collection.count() == 0:
            return []
        result = self.collection.query(query_embeddings=[embedding], n_results=min(top_k, self.collection.count()), include=["documents", "metadatas", "distances"])
        return [
            {"id": result["ids"][0][i], "text": result["documents"][0][i], "metadata": result["metadatas"][0][i], "distance": result["distances"][0][i]}
            for i in range(len(result["ids"][0]))
        ]

    def list_documents(self) -> list[dict[str, Any]]:
        result = self.collection.get(include=["metadatas"])
        grouped: dict[str, dict[str, Any]] = {}
        for metadata in result["metadatas"]:
            doc_hash = metadata["document_hash"]
            item = grouped.setdefault(doc_hash, {"hash": doc_hash, "filename": metadata["filename"], "chunks": 0, "characters": metadata.get("characters", 0)})
            item["chunks"] += 1
        return sorted(grouped.values(), key=lambda item: item["filename"].lower())

    def delete_document(self, document_hash: str) -> None:
        self.collection.delete(where={"document_hash": document_hash})

    def clear(self) -> None:
        self.client.delete_collection(self.COLLECTION)
        self.collection = self.client.get_or_create_collection(name=self.COLLECTION, metadata={"hnsw:space": "cosine"})
