"""Shared helpers for safe text processing and display."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def clean_text(text: str) -> str:
    """Normalize whitespace while retaining useful paragraph breaks."""
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", text)
    return text.strip()


def safe_filename(name: str) -> str:
    """Return a conservative filename, preventing path traversal."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name)[:160]


def format_distance(distance: float | None) -> str:
    if distance is None:
        return "n/a"
    # Chroma cosine distance: 0 is closest; this is a display-only estimate.
    return f"{max(0.0, min(1.0, 1 - distance / 2)):.0%} relevance"
