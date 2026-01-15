CHUNK_SIZE_CHARS: int = 2500
CHUNK_OVERLAP_CHARS: int = 300
TOP_K: int = 5
MAX_CHUNKS: int = 200

SYSTEM_PROMPT: str = (
    "You are a helpful assistant for Business Optima. "
    "Answer the user's question strictly using the provided document context. "
    "If the context is insufficient, say that the document does not contain "
    "enough information to answer the question. Be concise and professional."
)

