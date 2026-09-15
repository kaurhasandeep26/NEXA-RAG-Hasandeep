from src.document_manager import DocumentManager
from src.vector_store import VectorStore


class FakeEmbeddings:
    def embed(self, texts):
        return [[1.0, 0.0] for _ in texts]


def test_chromadb_retrieval_returns_chunk_and_source_metadata(tmp_path):
    store = VectorStore(str(tmp_path / "chroma"))
    store.add_chunks(
        ["doc:0"],
        ["ChromaDB persists vector embeddings."],
        [[1.0, 0.0]],
        [{"filename": "guide.txt", "document_hash": "doc", "chunk_index": 1}],
    )
    results = store.query([1.0, 0.0], top_k=4)
    assert results[0]["text"] == "ChromaDB persists vector embeddings."
    assert results[0]["metadata"]["filename"] == "guide.txt"
    assert results[0]["metadata"]["chunk_index"] == 1


def test_duplicate_document_is_not_indexed_twice(tmp_path):
    store = VectorStore(str(tmp_path / "chroma"))
    manager = DocumentManager(store, FakeEmbeddings())
    content = ("NEXA RAG indexes knowledge safely. " * 4).encode()
    first = manager.ingest("guide.txt", content, chunk_size=100, overlap=20)
    second = manager.ingest("guide.txt", content, chunk_size=100, overlap=20)
    assert first.status == "indexed"
    assert second.status == "duplicate"
    assert store.collection.count() == first.chunks
