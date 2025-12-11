# 🔧 Render Deployment Fix

## Issue
SQLAlchemy 2.0.23 is not compatible with Python 3.13, which Render uses by default.

## Solution Applied

1. **Upgraded SQLAlchemy** to version 2.0.36+ (compatible with Python 3.13)
2. **Created runtime.txt** to pin Python 3.11.9 (if not using Docker)
3. **Updated render.yaml** with correct Docker context

## Deployment Steps

### Option 1: Using Docker (Recommended)

1. **Update render.yaml** (already done):
   ```yaml
   services:
     - type: web
       name: knowledge-copilot-api
       env: docker
       dockerfilePath: ./Dockerfile
       dockerContext: ./backend
   ```

2. **In Render Dashboard:**
   - Go to your service settings
   - Make sure:
     - **Environment**: Docker
     - **Dockerfile Path**: `backend/Dockerfile`
     - **Root Directory**: `backend` (or leave empty if using dockerContext)

3. **Set Environment Variables:**
   ```
   GEMINI_API_KEY=your_actual_key_here
   ALLOWED_ORIGINS=https://your-frontend-domain.onrender.com
   DATABASE_URL=sqlite:///./knowledge_copilot.db
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   ```

4. **Add Persistent Disk:**
   - In Render dashboard → Your service → Settings
   - Add Persistent Disk:
     - Mount path: `/app/chroma_db`
     - Another mount: `/app/knowledge_copilot.db`

### Option 2: Using Python Buildpack (Alternative)

If Docker doesn't work, use Python buildpack:

1. **In Render Dashboard:**
   - Change Environment to: **Python 3**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **The runtime.txt file** will ensure Python 3.11.9 is used

## Important Notes

- **Port Binding**: Render automatically sets `$PORT` environment variable
- **Update main.py** if needed to use `$PORT` instead of hardcoded 8000
- **Persistent Storage**: Required for ChromaDB and SQLite to persist data

## Verify Deployment

After deployment:
1. Check logs in Render dashboard
2. Visit your service URL
3. Should see: `{"message": "Personal Knowledge Copilot API is running"}`

## Troubleshooting

If you still get SQLAlchemy errors:
1. Check Python version in logs
2. Ensure SQLAlchemy >= 2.0.36 is installed
3. Try clearing build cache in Render

