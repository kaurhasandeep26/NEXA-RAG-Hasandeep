"""Conversation-aware semantic retrieval."""
from __future__ import annotations

from src.embeddings import EmbeddingService
from src.vector_store import VectorStore


class Retriever:
    def __init__(self, store: VectorStore, embeddings: EmbeddingService) -> None:
        self.store, self.embeddings = store, embeddings

    def search(self, question: str, top_k: int, history: list[dict[str, str]] | None = None) -> list[dict]:
        # A little prior user context helps resolve follow-ups without sending history to storage.
        prior_questions = [item["content"] for item in (history or []) if item["role"] == "user"][-2:]
        query = " ".join(prior_questions + [question]) if len(question) < 80 and prior_questions else question
        return self.store.query(self.embeddings.embed([query])[0], top_k)
