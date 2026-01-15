from __future__ import annotations

from typing import List


def split_text(
    text: str,
    chunk_size: int,
    overlap: int,
    max_chunks: int | None = None,
) -> List[str]:
    """
    Simple, deterministic character-based splitter with overlap.
    Prefers splitting on paragraph boundaries when possible.
    """
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para).strip() if current else para
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            while len(para) > chunk_size:
                part = para[:chunk_size]
                chunks.append(part)
                para = para[chunk_size - overlap :]
            current = para

        if max_chunks and len(chunks) >= max_chunks:
            break

    if current and (not max_chunks or len(chunks) < max_chunks):
        chunks.append(current)

    if max_chunks:
        chunks = chunks[:max_chunks]

    return chunks

