"""Coordinates deduplicated document ingestion."""
from __future__ import annotations

from dataclasses import dataclass

from src.embeddings import EmbeddingService
from src.ingestion import extract_document, split_text
from src.utils import safe_filename, sha256_bytes
from src.vector_store import VectorStore


@dataclass
class IngestResult:
    filename: str
    status: str
    chunks: int = 0
    message: str = ""


class DocumentManager:
    def __init__(self, store: VectorStore, embeddings: EmbeddingService) -> None:
        self.store, self.embeddings = store, embeddings

    def ingest(self, filename: str, content: bytes, chunk_size: int, overlap: int) -> IngestResult:
        doc_hash = sha256_bytes(content)
        filename = safe_filename(filename)
        if self.store.document_exists(doc_hash):
            return IngestResult(filename, "duplicate", message="This exact document is already indexed.")
        extracted = extract_document(filename, content)
        chunks = split_text(extracted.text, chunk_size, overlap)
        if not chunks:
            return IngestResult(filename, "error", message="No usable chunks were produced.")
        ids = [f"{doc_hash}:{index}" for index in range(len(chunks))]
        metadata = [{"filename": filename, "document_hash": doc_hash, "chunk_index": index + 1, "characters": len(extracted.text)} for index in range(len(chunks))]
        self.store.add_chunks(ids, chunks, self.embeddings.embed(chunks), metadata)
        return IngestResult(filename, "indexed", len(chunks), "Indexed successfully.")
