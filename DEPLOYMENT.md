# Deployment Guide

## Backend Deployment (Render)

### Step 1: Prepare Backend

1. Ensure `Procfile` exists in the root directory with:
   ```
   web: uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

2. Ensure `requirements.txt` includes:
   - fastapi
   - uvicorn[standard]
   - python-multipart
   - google-generativeai
   - chromadb
   - pypdf
   - python-docx
   - numpy

### Step 2: Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `business-optima-rag-api` (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free tier is fine for testing

5. Add Environment Variables:
   - `GEMINI_API_KEY`: Your Gemini API key

6. Click "Create Web Service"
7. Wait for deployment to complete
8. Copy your service URL (e.g., `https://your-app.onrender.com`)

### Step 3: Update CORS (Optional)

In `app.py`, update the CORS origins to include your Vercel domain:
```python
allow_origins=["https://your-app.vercel.app"]
```

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Navigate to `business-chat-interface-main/`
2. Ensure `.gitignore` includes `.env.local` (it should already)

### Step 2: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Navigate to frontend directory:
   ```bash
   cd business-chat-interface-main
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy:
   ```bash
   vercel
   ```
   - Follow prompts
   - Set root directory to `business-chat-interface-main` if asked

5. Set environment variable:
   ```bash
   vercel env add VITE_API_URL
   ```
   - Enter your Render backend URL when prompted
   - Select "Production", "Preview", and "Development"

6. Redeploy to apply environment variable:
   ```bash
   vercel --prod
   ```

### Step 3: Deploy via Vercel Dashboard (Alternative)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `business-chat-interface-main`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `dist` (default)

5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: Your Render backend URL (e.g., `https://your-app.onrender.com`)
   - Apply to: Production, Preview, Development

6. Click "Deploy"

### Step 4: Verify Deployment

1. Visit your Vercel URL
2. Upload a test document (PDF, DOCX, or TXT)
3. Send a test message
4. Verify the response comes from your backend

## Local Development Setup

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GEMINI_API_KEY="your-key-here"  # Windows: set GEMINI_API_KEY=your-key-here

# Run server
python app.py
# Or: uvicorn app:app --reload
```

Backend runs on: `http://localhost:8000`

### Frontend

```bash
cd business-chat-interface-main

# Install dependencies
npm install

# Create .env.local file
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev
```

Frontend runs on: `http://localhost:8080`

## Troubleshooting

### Backend Issues

- **Port binding error**: Ensure `$PORT` is used in Procfile (Render sets this automatically)
- **CORS errors**: Update `allow_origins` in `app.py` to include your Vercel domain
- **Gemini API errors**: Verify `GEMINI_API_KEY` is set correctly in Render environment variables

### Frontend Issues

- **API connection errors**: Verify `VITE_API_URL` is set correctly in Vercel environment variables
- **Build errors**: Ensure all dependencies are installed (`npm install`)
- **Environment variable not working**: Restart dev server after changing `.env.local`

### Common Issues

- **Session not found**: Upload a document first to create a session
- **File upload fails**: Ensure file is PDF, DOCX, or TXT format
- **Slow responses**: Render free tier may spin down after inactivity; first request may be slow
