from __future__ import annotations

from typing import List, Tuple, Any

import numpy as np
import chromadb
from chromadb.config import Settings


def _get_client() -> chromadb.Client:
    return chromadb.Client(Settings(anonymized_telemetry=False, is_persistent=False))


def build_vector_store(embeddings: np.ndarray, chunks: List[str]) -> Any:
    if embeddings.size == 0 or not chunks:
        return None

    client = _get_client()
    # Ensure we don't fail if a collection with the same name already exists.
    # For this simple, in-memory setup we just recreate the collection each time.
    try:
        client.delete_collection("session-doc")
    except Exception:
        # It's fine if the collection doesn't exist yet.
        pass

    collection = client.create_collection(name="session-doc")
    ids = [str(i) for i in range(len(chunks))]
    collection.add(ids=ids, embeddings=embeddings.tolist(), documents=chunks)
    return collection


def query_vector_store(collection: Any, query_embedding: np.ndarray, top_k: int) -> List[Tuple[str, float]]:
    if collection is None or query_embedding.size == 0:
        return []

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
    )
    docs = results.get("documents", [[]])[0]
    dists = results.get("distances", [[]])[0]
    return list(zip(docs, dists))

