"""Central configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def _positive_int(name: str, default: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
        return value if value > 0 else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Runtime settings. Values can be overridden in `.env`."""

    root_dir: Path = ROOT_DIR
    chroma_path: Path = ROOT_DIR / os.getenv("NEXA_CHROMA_PATH", "vectorstore/chroma")
    upload_path: Path = ROOT_DIR / "data/uploads"
    embedding_model: str = os.getenv("NEXA_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    llm_model: str = os.getenv("NEXA_LLM_MODEL", "gpt-4o-mini")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or None
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL") or None
    default_top_k: int = _positive_int("NEXA_TOP_K", 4)
    default_chunk_size: int = _positive_int("NEXA_CHUNK_SIZE", 900)
    default_chunk_overlap: int = _positive_int("NEXA_CHUNK_OVERLAP", 160)

    def ensure_directories(self) -> None:
        self.chroma_path.mkdir(parents=True, exist_ok=True)
        self.upload_path.mkdir(parents=True, exist_ok=True)


settings = Settings()
