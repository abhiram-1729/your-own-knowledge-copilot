# 🚀 Render.com Deployment Guide

## Quick Fix Summary

The deployment failed due to **SQLAlchemy 2.0.23 incompatibility with Python 3.13**.

### ✅ Fixed:
1. Upgraded SQLAlchemy to `>=2.0.36` (Python 3.13 compatible)
2. Updated `main.py` to use `$PORT` environment variable
3. Fixed `render.yaml` Docker context
4. Created `runtime.txt` for Python version pinning

---

## Step-by-Step Deployment

### 1. Push Changes to GitHub

```bash
git add .
git commit -m "Fix Render deployment: Upgrade SQLAlchemy, add PORT support"
git push
```

### 2. Configure Render Service

#### Option A: Using Docker (Recommended)

1. **Go to Render Dashboard** → Your Service → Settings

2. **Service Settings:**
   - **Environment**: Docker
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Root Directory**: Leave empty (or set to `backend`)
   - **Docker Context**: `backend` (if using render.yaml, this is set automatically)

3. **Environment Variables:**
   Add these in Render dashboard:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   ALLOWED_ORIGINS=https://your-frontend.onrender.com,https://your-custom-domain.com
   DATABASE_URL=sqlite:///./knowledge_copilot.db
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   PORT=8000  # Render sets this automatically, but good to have
   ```

4. **Persistent Disk (IMPORTANT!):**
   - Go to: Settings → Persistent Disk
   - Add disk with mount path: `/app/chroma_db`
   - Add another disk for: `/app/knowledge_copilot.db`
   - **Without this, your data will be lost on every deploy!**

5. **Health Check:**
   - Health Check Path: `/`
   - Should return: `{"message": "Personal Knowledge Copilot API is running"}`

#### Option B: Using Python Buildpack (If Docker doesn't work)

1. **Service Settings:**
   - **Environment**: Python 3
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Python Version:**
   - The `runtime.txt` file will ensure Python 3.11.9 is used

---

## 3. Deploy

1. **Manual Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

2. **Auto Deploy:**
   - Render will auto-deploy on every push to your main branch

---

## 4. Verify Deployment

After deployment completes:

1. **Check Logs:**
   - Go to "Logs" tab
   - Should see: `Application startup complete`
   - No SQLAlchemy errors

2. **Test Endpoint:**
   ```bash
   curl https://your-service.onrender.com/
   ```
   Should return: `{"message": "Personal Knowledge Copilot API is running"}`

3. **Check Health:**
   - Service status should be "Live" (green)

---

## Common Issues & Solutions

### Issue: "No open ports detected"

**Solution:**
- Make sure `main.py` uses `os.getenv("PORT", 8000)`
- Render sets `$PORT` automatically
- The fix has been applied ✅

### Issue: SQLAlchemy AssertionError

**Solution:**
- SQLAlchemy upgraded to >=2.0.36 ✅
- If still occurs, check Python version in logs
- Ensure Dockerfile uses Python 3.11.9

### Issue: Data not persisting

**Solution:**
- Add Persistent Disk in Render settings
- Mount paths: `/app/chroma_db` and `/app/knowledge_copilot.db`

### Issue: CORS errors

**Solution:**
- Update `ALLOWED_ORIGINS` environment variable
- Include your frontend URL: `https://your-frontend.onrender.com`

### Issue: Build fails

**Solution:**
- Check build logs for specific errors
- Ensure all dependencies in `requirements.txt`
- Try clearing build cache

---

## Environment Variables Reference

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | `AIzaSy...` | Your Gemini API key |
| `ALLOWED_ORIGINS` | ✅ Yes | `https://app.onrender.com` | Comma-separated frontend URLs |
| `DATABASE_URL` | ⚠️ Optional | `sqlite:///./knowledge_copilot.db` | Database connection string |
| `CHROMA_PERSIST_DIRECTORY` | ⚠️ Optional | `./chroma_db` | ChromaDB storage path |
| `PORT` | ❌ No | `8000` | Set automatically by Render |

---

## Next Steps After Deployment

1. **Deploy Frontend:**
   - Create new Static Site service
   - Set `VITE_API_URL` to your backend URL
   - Build command: `npm install && npm run build`

2. **Update CORS:**
   - Add frontend URL to `ALLOWED_ORIGINS`

3. **Test Full Stack:**
   - Upload a document
   - Ask a question
   - Verify everything works

---

## Support

If deployment still fails:
1. Check Render logs for specific errors
2. Verify all environment variables are set
3. Ensure Persistent Disk is configured
4. Check that Dockerfile builds successfully locally

**The SQLAlchemy issue should now be resolved!** 🎉

