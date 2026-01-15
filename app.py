import os
import hashlib
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.document_loader import load_document_from_bytes
from rag.text_splitter import split_text
from rag.embeddings import embed_chunks, get_query_embedding, ensure_gemini_client
from rag.vector_store import build_vector_store, query_vector_store
from config.settings import (
    CHUNK_SIZE_CHARS,
    CHUNK_OVERLAP_CHARS,
    TOP_K,
    MAX_CHUNKS,
)
from rag.chat_engine import generate_answer

# Initialize FastAPI app
app = FastAPI(title="Business Optima RAG API")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client on startup
ensure_gemini_client()

# In-memory session storage (in production, consider Redis or database)
sessions: Dict[str, Dict[str, Any]] = {}
SESSION_TIMEOUT = timedelta(hours=24)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


class UploadResponse(BaseModel):
    session_id: str
    doc_name: str
    message: str


def _get_or_create_session(session_id: Optional[str] = None) -> str:
    """Get existing session or create a new one."""
    if session_id and session_id in sessions:
        return session_id
    
    new_session_id = str(uuid.uuid4())
    sessions[new_session_id] = {
        "messages": [],
        "doc_text": None,
        "doc_chunks": [],
        "vector_store": None,
        "doc_hash": None,
        "doc_name": None,
        "ready": False,
        "created_at": datetime.now(),
    }
    return new_session_id


def _hash_file_bytes(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


@app.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    session_id: Optional[str] = None,
):
    """
    Upload a document (PDF, DOCX, or TXT) for RAG processing.
    Returns a session_id that should be used for subsequent chat requests.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Validate file type
    suffix = file.filename.lower().split(".")[-1]
    if suffix not in ["pdf", "docx", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, or TXT files."
        )
    
    # Read file bytes
    file_bytes = await file.read()
    file_hash = _hash_file_bytes(file_bytes)
    
    # Get or create session
    session_id = _get_or_create_session(session_id)
    session = sessions[session_id]
    
    # Check if same file is already uploaded
    if session["doc_hash"] == file_hash:
        return UploadResponse(
            session_id=session_id,
            doc_name=session["doc_name"] or file.filename,
            message="Document already processed."
        )
    
    # Reset document state
    session["doc_text"] = None
    session["doc_chunks"] = []
    session["vector_store"] = None
    session["ready"] = False
    session["messages"] = []
    
    try:
        # Load document
        text, meta = load_document_from_bytes(file_bytes, file.filename)
        session["doc_text"] = text
        session["doc_name"] = meta.get("name", file.filename)
        session["doc_hash"] = file_hash
        
        # Split into chunks
        chunks = split_text(
            text,
            chunk_size=CHUNK_SIZE_CHARS,
            overlap=CHUNK_OVERLAP_CHARS,
            max_chunks=MAX_CHUNKS,
        )
        session["doc_chunks"] = chunks
        
        # Generate embeddings and build vector store
        embeddings = embed_chunks(chunks)
        vector_store = build_vector_store(embeddings, chunks)
        session["vector_store"] = vector_store
        session["ready"] = True
        
        return UploadResponse(
            session_id=session_id,
            doc_name=session["doc_name"],
            message="Document processed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a chat message and get RAG-based response.
    Requires a valid session_id from /upload endpoint.
    """
    session_id = request.session_id
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found. Please upload a document first.")
    
    session = sessions[session_id]
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Add user message to history
    session["messages"].append({"role": "user", "content": request.message})
    
    # Check if document is ready
    if not session["ready"] or not session["vector_store"]:
        error_msg = "Please upload a PDF, DOCX, or TXT document first so I can answer based on its content."
        session["messages"].append({"role": "assistant", "content": error_msg})
        return ChatResponse(
            session_id=session_id,
            response=error_msg
        )
    
    try:
        # Get query embedding
        query_embedding = get_query_embedding(request.message)
        
        # Query vector store
        retrieved_chunks = query_vector_store(
            session["vector_store"],
            query_embedding,
            top_k=TOP_K,
        )
        
        # Generate answer
        answer = generate_answer(
            question=request.message,
            retrieved_chunks=retrieved_chunks,
            chat_history=session["messages"],
        )
        
        # Add assistant message to history
        session["messages"].append({"role": "assistant", "content": answer})
        
        return ChatResponse(
            session_id=session_id,
            response=answer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

