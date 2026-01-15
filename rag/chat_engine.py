from __future__ import annotations

from typing import List, Dict, Tuple

import google.generativeai as genai

from config.settings import SYSTEM_PROMPT


def _build_context(retrieved_chunks: List[Tuple[str, float]]) -> str:
    parts = []
    for idx, (chunk, _) in enumerate(retrieved_chunks, start=1):
        parts.append(f"Source #{idx}:\n{chunk}")
    return "\n\n".join(parts)


def generate_answer(
    question: str,
    retrieved_chunks: List[Tuple[str, float]],
    chat_history: List[Dict[str, str]],
) -> str:
    if not retrieved_chunks:
        return (
            "I could not retrieve any relevant context from the document. "
            "Please try rephrasing your question or upload a different document."
        )

    context_block = _build_context(retrieved_chunks)

    messages = [
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {
            "role": "user",
            "parts": [
                "Here is context extracted from the document:\n\n"
                f"{context_block}\n\n"
                "Answer the question strictly using only this context.",
            ],
        },
    ]

    messages.append({"role": "user", "parts": [question]})

    # Use updated Gemini model as requested
    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(messages)
    return response.text or "Sorry, I could not generate an answer."

