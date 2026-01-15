# Quick Start Guide

## Local Development

### 1. Backend Setup (Terminal 1)

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
# Windows PowerShell:
#   $env:GEMINI_API_KEY="your-gemini-api-key-here"
# Windows CMD:
#   set GEMINI_API_KEY=your-gemini-api-key-here
# Mac/Linux:
export GEMINI_API_KEY="your-gemini-api-key-here"

# Run server
python app.py
```

Backend will be available at: `http://localhost:8000`

### 2. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd business-chat-interface-main

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev
```

Frontend will be available at: `http://localhost:8080`

### 3. Test the Application

1. Open `http://localhost:8080` in your browser
2. Click the "+" button to upload a PDF, DOCX, or TXT file
3. Wait for "Document loaded" message
4. Type a question and press Enter
5. Get your RAG-powered answer!

## API Endpoints Reference

### Upload Document
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

Response:
```json
{
  "session_id": "uuid-here",
  "doc_name": "document.pdf",
  "message": "Document processed successfully."
}
```

### Send Chat Message
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid-from-upload",
    "message": "What is this document about?"
  }'
```

Response:
```json
{
  "session_id": "uuid-here",
  "response": "Answer from RAG system..."
}
```

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok"
}
```

## Environment Variables

### Backend
- `GEMINI_API_KEY` (required) - Your Google Gemini API key

### Frontend
- `VITE_API_URL` (optional) - Backend URL, defaults to `http://localhost:8000`

## Troubleshooting

**Backend won't start:**
- Check that `GEMINI_API_KEY` is set
- Verify Python version (3.8+)
- Ensure all dependencies are installed

**Frontend can't connect to backend:**
- Verify backend is running on port 8000
- Check `VITE_API_URL` in `.env.local`
- Check browser console for CORS errors

**File upload fails:**
- Ensure file is PDF, DOCX, or TXT
- Check file size (very large files may timeout)
- Verify backend is running and accessible

**Chat doesn't work:**
- Make sure you uploaded a document first
- Check that session_id is being used correctly
- Verify backend logs for errors
