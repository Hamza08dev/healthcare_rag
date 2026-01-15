## Business Optima Document Chatbot (FastAPI + React + Gemini RAG)

This app is a document chatbot for Business Optima with a React frontend and FastAPI backend.
Users upload a PDF, DOCX, or TXT file and ask questions. The app indexes the
document with Gemini embeddings and answers using retrieved context.

### Architecture

- **Frontend**: React + TypeScript + Vite (in `business-chat-interface-main/`)
- **Backend**: FastAPI (Python) with RAG logic
- **Deployment**: Frontend on Vercel, Backend on Render

### Running locally

#### Backend

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Gemini API key:
```bash
export GEMINI_API_KEY="your-key-here"  # On Windows: set GEMINI_API_KEY=your-key-here
```

4. Start the FastAPI server:
```bash
python app.py
# Or: uvicorn app:app --reload
```

The backend will run on `http://localhost:8000`

#### Frontend

1. Navigate to the frontend directory:
```bash
cd business-chat-interface-main
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file (or use `.env.example`):
```bash
VITE_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:8080` (or the port shown in terminal)

### Deployment

#### Backend (Render)

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `GEMINI_API_KEY`
5. Deploy

The backend URL will be something like: `https://your-app.onrender.com`

#### Frontend (Vercel)

1. Navigate to the frontend directory:
```bash
cd business-chat-interface-main
```

2. Install Vercel CLI (if not installed):
```bash
npm i -g vercel
```

3. Deploy:
```bash
vercel
```

4. Set environment variable in Vercel dashboard:
   - Go to your project settings
   - Add environment variable: `VITE_API_URL` = `https://your-backend.onrender.com`

Or deploy via Vercel dashboard:
1. Import your GitHub repository
2. Set root directory to `business-chat-interface-main`
3. Add environment variable `VITE_API_URL` pointing to your Render backend URL
4. Deploy

### API Endpoints

- `POST /upload` - Upload a document (PDF, DOCX, TXT)
  - Form data: `file` (required), `session_id` (optional)
  - Returns: `{ session_id, doc_name, message }`

- `POST /chat` - Send a chat message
  - Body: `{ session_id, message }`
  - Returns: `{ session_id, response }`

- `GET /health` - Health check endpoint

### Notes

- The app uses in-memory, per-session vector stores only; there is no persistent database or cross-session state.
- Sessions expire after 24 hours of inactivity.
- CORS is configured to allow all origins. In production, restrict this to your Vercel domain.

