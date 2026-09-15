from types import SimpleNamespace

import pytest

from src.rag_chain import GeminiGenerationError, RAGChain, SYSTEM_PROMPT, build_prompt


SOURCES = [{"text": "NEXA uses ChromaDB for retrieval.", "metadata": {"filename": "guide.txt", "chunk_index": 2}}]


def test_prompt_contains_only_retrieved_context_question_and_source_label():
    prompt = build_prompt("What stores vectors?", SOURCES)
    assert "NEXA uses ChromaDB" in prompt
    assert "[Source 1: guide.txt, chunk 2]" in prompt
    assert "What stores vectors?" in prompt
    assert "OPENAI" not in prompt


def test_system_prompt_resists_document_prompt_injection():
    assert "untrusted" in SYSTEM_PROMPT.lower()
    assert "Never follow instructions" in SYSTEM_PROMPT
    assert "Do not invent citations" in SYSTEM_PROMPT


def test_empty_retrieval_returns_grounded_fallback_without_api_call():
    assert RAGChain("test-key", "test-model").answer("Anything?", [], []) == "I could not find sufficient information in the uploaded knowledge."


def test_missing_key_has_clear_configuration_message():
    with pytest.raises(GeminiGenerationError, match="not configured"):
        RAGChain(None, "test-model").answer("Anything?", SOURCES, [])


def test_gemini_generation_uses_grounded_prompt_and_extracts_text(monkeypatch):
    calls = {}

    class FakeClient:
        def __init__(self, api_key):
            calls["api_key"] = api_key
            self.models = self

        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(text="ChromaDB stores the vectors [Source 1].")

    monkeypatch.setattr("src.rag_chain.genai.Client", FakeClient)
    answer = RAGChain("test-key", "test-model").answer("What stores vectors?", SOURCES, [])
    assert answer == "ChromaDB stores the vectors [Source 1]."
    assert calls["api_key"] == "test-key"
    assert calls["model"] == "test-model"
    assert "NEXA uses ChromaDB" in calls["contents"]


@pytest.mark.parametrize("failure, expected", [
    (RuntimeError("401 authentication failed"), "authenticate"),
    (RuntimeError("429 quota exceeded"), "quota or rate limit"),
    (RuntimeError("network timeout"), "could not be reached"),
])
def test_gemini_api_failures_are_user_friendly(monkeypatch, failure, expected):
    class FakeClient:
        def __init__(self, api_key):
            self.models = self

        def generate_content(self, **kwargs):
            raise failure

    monkeypatch.setattr("src.rag_chain.genai.Client", FakeClient)
    with pytest.raises(GeminiGenerationError, match=expected):
        RAGChain("test-key", "test-model").answer("Anything?", SOURCES, [])


def test_empty_gemini_response_is_handled(monkeypatch):
    class FakeClient:
        def __init__(self, api_key):
            self.models = self

        def generate_content(self, **kwargs):
            return SimpleNamespace(text=" ")

    monkeypatch.setattr("src.rag_chain.genai.Client", FakeClient)
    with pytest.raises(GeminiGenerationError, match="empty response"):
        RAGChain("test-key", "test-model").answer("Anything?", SOURCES, [])
