from __future__ import annotations

from typing import List

import os

import numpy as np
import google.generativeai as genai


_CLIENT_INITIALIZED = False
# Use updated embedding model as requested
_EMBED_MODEL = "models/gemini-embedding-001"


def ensure_gemini_client() -> None:
    global _CLIENT_INITIALIZED
    if _CLIENT_INITIALIZED:
        return
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Allow Streamlit secrets pattern as a fallback without importing streamlit here
        try:
            import streamlit as st  # type: ignore

            api_key = st.secrets.get("GEMINI_API_KEY", "")  # type: ignore[attr-defined]
        except Exception:
            api_key = ""
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Configure it as an environment variable or in Streamlit secrets."
        )
    genai.configure(api_key=api_key)
    _CLIENT_INITIALIZED = True


def embed_chunks(chunks: List[str]) -> np.ndarray:
    if not chunks:
        return np.zeros((0, 0), dtype="float32")

    ensure_gemini_client()
    result = genai.embed_content(
        model=_EMBED_MODEL,
        content=chunks,
        task_type="retrieval_document",
    )
    embeddings = np.asarray(result["embedding"], dtype="float32")
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)
    return embeddings


def get_query_embedding(query: str) -> np.ndarray:
    ensure_gemini_client()
    result = genai.embed_content(
        model=_EMBED_MODEL,
        content=query,
        task_type="retrieval_query",
    )
    emb = np.asarray(result["embedding"], dtype="float32")
    if emb.ndim == 1:
        emb = emb.reshape(1, -1)
    return emb

