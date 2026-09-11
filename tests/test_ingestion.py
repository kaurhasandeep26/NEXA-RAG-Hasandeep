from src.ingestion import IngestionError, extract_document, split_text


def test_split_text_preserves_all_content():
    text = "Sentence one. " * 100
    chunks = split_text(text, chunk_size=180, overlap=30)
    assert len(chunks) > 2
    assert chunks[0].startswith("Sentence one")
    assert chunks[-1].endswith("one.")


def test_invalid_extension_is_rejected():
    try:
        extract_document("bad.exe", b"hello")
    except IngestionError as exc:
        assert "PDF, TXT, and DOCX" in str(exc)
    else:
        raise AssertionError("Expected IngestionError")


def test_empty_file_is_rejected():
    try:
        extract_document("empty.txt", b"")
    except IngestionError as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("Expected IngestionError")
