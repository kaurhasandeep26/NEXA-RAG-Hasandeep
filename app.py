"""NEXA-RAG Streamlit application."""
from __future__ import annotations

import logging

import streamlit as st

from src.config import settings
from src.document_manager import DocumentManager
from src.embeddings import EmbeddingService
from src.ingestion import IngestionError
from src.rag_chain import RAGChain
from src.retriever import Retriever
from src.utils import format_distance
from src.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

st.set_page_config(page_title="NEXA-RAG | Knowledge Assistant", page_icon="✦", layout="wide")

@st.cache_resource(show_spinner=False)
def services():
    settings.ensure_directories()
    embedding_service = EmbeddingService(settings.embedding_model)
    store = VectorStore(str(settings.chroma_path))
    return store, embedding_service, DocumentManager(store, embedding_service), Retriever(store, embedding_service)

def source_panel(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander("Sources & retrieval details", expanded=False):
        for index, source in enumerate(sources, 1):
            meta = source["metadata"]
            st.markdown(f"**Source {index} · {meta['filename']} · chunk {meta['chunk_index']}** — {format_distance(source['distance'])}")
            st.caption(source["text"][:650] + ("…" if len(source["text"]) > 650 else ""))

def main() -> None:
    st.markdown("""<style>
    .block-container {max-width: 1250px; padding-top: 2rem;} .hero {padding: 1.4rem 1.7rem; border-radius: 18px; background: linear-gradient(110deg,#111c42,#352169); color:white; margin-bottom:1.2rem;} .hero h1 {margin:0; font-size:2.3rem;} .hero p {margin:.35rem 0 0; opacity:.86;} [data-testid='stSidebar'] {border-right:1px solid #e8e8ef;}
    </style>""", unsafe_allow_html=True)
    st.markdown("<div class='hero'><h1>✦ NEXA-RAG</h1><p>Your private, grounded knowledge assistant. Upload documents. Ask with confidence.</p></div>", unsafe_allow_html=True)
    store, _, manager, retriever = services()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Knowledge Studio")
        uploaded = st.file_uploader("Add knowledge", type=["pdf", "txt", "docx"], accept_multiple_files=True, help="Files stay local in this project folder.")
        with st.expander("Retrieval settings"):
            top_k = st.slider("Sources to retrieve", 1, 10, settings.default_top_k)
            chunk_size = st.slider("Chunk size (characters)", 300, 1800, settings.default_chunk_size, 50)
            overlap = st.slider("Chunk overlap", 0, min(500, chunk_size - 1), min(settings.default_chunk_overlap, chunk_size - 1), 20)
        if st.button("Index selected documents", type="primary", use_container_width=True, disabled=not uploaded):
            progress = st.progress(0, text="Preparing documents…")
            for i, file in enumerate(uploaded or []):
                try:
                    with st.spinner(f"Indexing {file.name}…"):
                        result = manager.ingest(file.name, file.getvalue(), chunk_size, overlap)
                    if result.status == "indexed": st.success(f"{result.filename}: {result.chunks} chunks indexed")
                    else: st.info(f"{result.filename}: {result.message}")
                except (IngestionError, ValueError) as exc: st.error(f"{file.name}: {exc}")
                except Exception as exc: logging.exception("Indexing failed"); st.error(f"{file.name}: indexing failed ({exc})")
                progress.progress((i + 1) / len(uploaded), text="Indexing complete" if i + 1 == len(uploaded) else "Indexing documents…")
            st.rerun()
        st.divider()
        st.subheader("Indexed documents")
        documents = store.list_documents()
        if documents:
            for doc in documents:
                left, right = st.columns([4, 1])
                left.caption(f"📄 {doc['filename']}\n{doc['chunks']} chunks")
                if right.button("✕", key=doc["hash"], help="Remove this document and its vectors"):
                    store.delete_document(doc["hash"]); st.rerun()
        else: st.caption("No documents indexed yet.")
        if st.button("Clear chat", use_container_width=True): st.session_state.messages = []; st.rerun()
        with st.expander("About NEXA-RAG"):
            st.write("A local-first Retrieval-Augmented Generation assistant that grounds answers in your uploaded knowledge.")
            st.caption("Built by Hasandeep Kaur")

    if not settings.openai_api_key:
        st.warning("Generation is not configured. Copy `.env.example` to `.env` and add `OPENAI_API_KEY`. You can still index and inspect retrieval results.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant": source_panel(message.get("sources", []))
    question = st.chat_input("Ask anything about your uploaded knowledge…", disabled=not documents)
    if question:
        with st.chat_message("user"): st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("assistant"):
            with st.spinner("Searching your knowledge base…"):
                try:
                    sources = retriever.search(question, top_k, st.session_state.messages[:-1])
                    answer = RAGChain(settings.openai_api_key, settings.llm_model, settings.openai_base_url).answer(question, sources, st.session_state.messages[:-1])
                    st.markdown(answer); source_panel(sources)
                except Exception as exc:
                    logging.exception("Question answering failed")
                    answer, sources = f"I ran into a problem while answering: {exc}", []
                    st.error(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
    elif not documents:
        st.info("Start by uploading one or more PDF, TXT, or DOCX files in the Knowledge Studio.")

if __name__ == "__main__":
    main()
