# NEXA-RAG ✦

> A polished, local-first Retrieval-Augmented Generation knowledge assistant built by **Hasandeep Kaur**.

NEXA-RAG turns a collection of PDFs, TXT files, and DOCX files into a searchable private knowledge base. It retrieves the most relevant passages before asking an LLM to answer, so responses are grounded in your own documents and include inspectable sources.

## Highlights

- Multi-document PDF, TXT, and DOCX ingestion with validation and text cleaning
- Local persistent ChromaDB vector store with Sentence Transformers embeddings
- Semantic, conversation-aware retrieval with adjustable top-k, chunk size, and overlap
- Grounded Google Gemini answers with source labels and retrieval/relevance details
- Duplicate protection using content hashes, per-document removal, safe re-indexing, and clear chat
- Prompt-injection-aware system instructions: documents are treated as untrusted reference material
- Modern Streamlit product interface, progress feedback, friendly errors, and local-first storage

## Architecture

```text
Upload → extract/clean → intelligent chunks → Sentence Transformers embeddings
       → persistent ChromaDB → semantic retrieval → grounded LLM answer + citations
```

The UI (`app.py`) is deliberately separated from ingestion, embeddings, storage, retrieval, and generation services in `src/` so each layer is easy to test or replace.

## Technology stack

Python · Streamlit · ChromaDB · Sentence Transformers · Google Gemini API · PyMuPDF · python-docx · python-dotenv · pytest

## Project structure

```text
NEXA-RAG/
├── app.py                 # Streamlit user interface
├── src/                   # Modular application services
├── tests/                 # Fast ingestion tests
├── data/uploads/          # Reserved for local source files (ignored by Git)
├── vectorstore/chroma/    # Persistent local vector database (ignored by Git)
├── .env.example           # Safe environment-variable template
└── requirements.txt
```

## Quick start

1. Install Python 3.11–3.14, then open a terminal in this project folder.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the application:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create a Gemini API key in Google AI Studio. Copy `.env.example` to `.env`, then set your key:

   ```env
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   GEMINI_MODEL=gemini-2.5-flash
   ```

5. Run it:

   ```powershell
   streamlit run app.py
   ```

Open the local URL Streamlit prints, upload documents, click **Index selected documents**, and ask questions.

### Environment variables

| Variable | Required | Purpose |
|---|---:|---|
| `GEMINI_API_KEY` | For generated answers | Gemini API key, loaded from `.env` or Streamlit secrets |
| `GEMINI_MODEL` | No | Defaults to `gemini-2.5-flash` |
| `NEXA_EMBEDDING_MODEL` | No | Defaults to `all-MiniLM-L6-v2` |
| `NEXA_CHROMA_PATH` | No | Local persistent vector-store location |

The first indexing run downloads the selected Sentence Transformers model. This is normal; afterward it is cached locally. Your documents and vectors remain on your computer. Do not commit `.env`, `data/uploads`, or `vectorstore/chroma`.

### Streamlit Community Cloud

In your deployed app, open **Settings → Secrets** and add the following (with your real key only in the secret manager):

```toml
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-2.5-flash"
```

Never add this key to the repository. If the key is absent, NEXA-RAG still supports document indexing and retrieval, while generation shows a friendly configuration message.

## Testing

Run the fast checks after installing dependencies:

```powershell
python -m compileall app.py src tests
python -m pytest -q
```

## Screenshots / demo

_Add screenshots or a short screen recording here before sharing on LinkedIn or GitHub._

## Future improvements

- Add OCR for scanned PDFs
- Support local LLM providers such as Ollama
- Add collections/workspaces and metadata filters
- Stream tokens, export chats, and add evaluation datasets

## Portfolio description

**NEXA-RAG** is a portfolio-ready AI knowledge assistant that demonstrates document processing, embedding-based semantic search, persistent vector databases, retrieval-grounded generation, and production-minded UX safeguards.
