# ⚡ Quick Start - Deploy to Cloud

## 🚀 Fastest Way to Deploy

### Option 1: Render.com (Recommended for Beginners)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Deploy Backend on Render**
   - Visit https://dashboard.render.com
   - New → Web Service
   - Connect GitHub repo
   - Settings:
     - **Root Directory**: `backend`
     - **Dockerfile Path**: `backend/Dockerfile`
     - **Environment**: Docker
   - Add Environment Variables:
     ```
     GEMINI_API_KEY=your_key_here
     ALLOWED_ORIGINS=https://your-frontend.onrender.com
     ```
   - Add Persistent Disk:
     - Mount: `/app/chroma_db`
     - Mount: `/app/knowledge_copilot.db`

3. **Deploy Frontend on Render**
   - New → Static Site
   - Connect GitHub repo
   - Settings:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`
   - Add Environment Variable:
     ```
     VITE_API_URL=https://your-backend.onrender.com
     ```

4. **Done!** Your app is live! 🎉

---

### Option 2: Docker Compose (Any VPS/Cloud)

1. **Get a VPS** (DigitalOcean, AWS EC2, Linode, etc.)

2. **SSH into server**
   ```bash
   ssh user@your-server-ip
   ```

3. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

4. **Clone and Deploy**
   ```bash
   git clone <your-repo-url>
   cd your-own-knowledge-copilot/backend
   nano .env  # Add GEMINI_API_KEY and other vars
   cd ..
   docker-compose up -d
   ```

5. **Set up Nginx** (for SSL and domain)
   ```bash
   sudo apt install nginx certbot python3-certbot-nginx
   # Configure nginx to proxy to localhost:3000 (frontend) and :8000 (backend)
   sudo certbot --nginx -d your-domain.com
   ```

---

## 📝 Environment Variables Checklist

### Backend (.env)
```
✅ GEMINI_API_KEY=your_key_here (REQUIRED)
✅ ALLOWED_ORIGINS=https://your-frontend-domain.com
✅ DATABASE_URL=sqlite:///./knowledge_copilot.db
✅ CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### Frontend (.env)
```
✅ VITE_API_URL=https://your-backend-domain.com
```

---

## 🔍 Verify Deployment

1. **Check Backend**: Visit `https://your-backend.com/`
   - Should see: `{"message": "Personal Knowledge Copilot API is running"}`

2. **Check Frontend**: Visit `https://your-frontend.com`
   - Should see the Knowledge Copilot UI

3. **Test Upload**: Try uploading a document

4. **Test Query**: Ask a question about uploaded documents

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| CORS Error | Update `ALLOWED_ORIGINS` in backend `.env` |
| API Connection Failed | Check `VITE_API_URL` in frontend |
| Data Not Persisting | Ensure persistent volumes/storage mounted |
| Build Fails | Check logs: `docker-compose logs` |

---

## 📚 Full Documentation

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed guides for all platforms.

---

**Need Help?** Check the troubleshooting section in DEPLOYMENT.md

