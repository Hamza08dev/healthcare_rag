# How to Set Up Gemini API Key

## Step 1: Get Your Gemini API Key

If you don't have a Gemini API key yet:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (it will look like: `AIzaSy...`)

**Important**: Keep your API key secret! Never commit it to GitHub or share it publicly.

## Step 2: Set API Key for Local Development

### Option A: Windows (PowerShell or Command Prompt)

**PowerShell:**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python app.py
```

**Command Prompt (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

**Note**: This sets the variable for the current terminal session only. If you close the terminal, you'll need to set it again.

### Option B: Windows (Permanent - User Environment Variable)

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → "Environment Variables"
3. Under "User variables", click "New"
4. Variable name: `GEMINI_API_KEY`
5. Variable value: `your-api-key-here`
6. Click OK on all dialogs
7. Restart your terminal/PowerShell

### Option C: Create a `.env` File (Recommended for Development)

1. Create a file named `.env` in the project root (same folder as `app.py`)
2. Add this line:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```
3. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```
4. Update `app.py` to load from `.env` (see below)

**Update app.py to support .env file:**

Add this near the top of `app.py` (after imports):
```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
```

Then add `python-dotenv` to `requirements.txt`:
```
python-dotenv>=1.0.0
```

### Option D: Mac/Linux

**Bash/Zsh:**
```bash
export GEMINI_API_KEY="your-api-key-here"
python app.py
```

**Make it permanent** (add to `~/.bashrc` or `~/.zshrc`):
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Step 3: Verify API Key is Set

### Windows PowerShell:
```powershell
echo $env:GEMINI_API_KEY
```

### Windows CMD:
```cmd
echo %GEMINI_API_KEY%
```

### Mac/Linux:
```bash
echo $GEMINI_API_KEY
```

You should see your API key printed (or nothing if it's not set).

## Step 4: Test the Backend

Run the backend:
```bash
python app.py
```

If the API key is set correctly, you should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

If you see an error about `GEMINI_API_KEY`, the key is not set correctly.

## Step 5: Set API Key for Production (Render)

When deploying to Render:

1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Key: `GEMINI_API_KEY`
6. Value: `your-api-key-here`
7. Click "Save Changes"
8. Render will automatically redeploy

**Important**: Never hardcode your API key in the code! Always use environment variables.

## Troubleshooting

### Error: "GEMINI_API_KEY is not set"

**Solution**: Make sure you've set the environment variable before running `python app.py`

**Windows**: Use `set` (CMD) or `$env:` (PowerShell)  
**Mac/Linux**: Use `export`

### Error: "Invalid API key"

**Solution**: 
- Verify your API key is correct (no extra spaces)
- Make sure you copied the entire key
- Check that the API key hasn't been revoked in Google AI Studio

### API Key works locally but not on Render

**Solution**:
- Double-check the environment variable is set in Render dashboard
- Make sure there are no typos in the variable name (`GEMINI_API_KEY`)
- Redeploy after setting the variable

### Want to use .env file?

1. Install python-dotenv: `pip install python-dotenv`
2. Add to `requirements.txt`: `python-dotenv>=1.0.0`
3. Add to top of `app.py`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
4. Create `.env` file with: `GEMINI_API_KEY=your-key`
5. Add `.env` to `.gitignore` (don't commit it!)

## Quick Reference

| Platform | Command |
|----------|---------|
| Windows PowerShell | `$env:GEMINI_API_KEY="key"` |
| Windows CMD | `set GEMINI_API_KEY=key` |
| Mac/Linux | `export GEMINI_API_KEY="key"` |
| Render | Set in dashboard → Environment tab |
| Vercel | Not needed (frontend doesn't use API key) |
