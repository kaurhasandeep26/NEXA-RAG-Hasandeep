from src.config import Settings


def test_gemini_settings_read_environment(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    configured = Settings()
    assert configured.gemini_api_key == "test-key"
    assert configured.gemini_model == "test-model"


def test_missing_gemini_key_is_none(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert Settings().gemini_api_key is None
