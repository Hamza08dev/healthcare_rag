from __future__ import annotations

from typing import Tuple, Dict, Any

from io import BytesIO

import pypdf
import docx  # type: ignore


def _load_pdf(file_bytes: bytes, name: str) -> Tuple[str, Dict[str, Any]]:
    reader = pypdf.PdfReader(BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    text = "\n\n".join(texts)
    meta = {"name": name, "pages": len(reader.pages)}
    return text, meta


def _load_docx(file_bytes: bytes, name: str) -> Tuple[str, Dict[str, Any]]:
    document = docx.Document(BytesIO(file_bytes))
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    text = "\n\n".join(paragraphs)
    meta = {"name": name, "paragraphs": len(paragraphs)}
    return text, meta


def _load_txt(file_bytes: bytes, name: str) -> Tuple[str, Dict[str, Any]]:
    text = file_bytes.decode("utf-8", errors="ignore")
    meta = {"name": name, "length": len(text)}
    return text, meta


def load_document(uploaded_file) -> Tuple[str, Dict[str, Any]]:
    """
    Load a Streamlit UploadedFile (PDF, DOCX, or TXT) and return plain text and metadata.
    """
    file_bytes = uploaded_file.getvalue()
    name = getattr(uploaded_file, "name", "document")
    return load_document_from_bytes(file_bytes, name)


def load_document_from_bytes(file_bytes: bytes, name: str) -> Tuple[str, Dict[str, Any]]:
    """
    Load a document from bytes (PDF, DOCX, or TXT) and return plain text and metadata.
    Works with FastAPI UploadFile.
    """
    suffix = name.lower().split(".")[-1]

    if suffix == "pdf":
        text, meta = _load_pdf(file_bytes, name)
    elif suffix == "docx":
        text, meta = _load_docx(file_bytes, name)
    else:
        text, meta = _load_txt(file_bytes, name)

    text = " ".join(text.split())
    return text, meta

