# 🚀 Deployment Guide - Knowledge Copilot

Complete guide to deploy your Knowledge Copilot application to the cloud using FastAPI and Docker.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Docker Deployment](#local-docker-deployment)
3. [Cloud Deployment Options](#cloud-deployment-options)
   - [Render.com](#rendercom)
   - [Railway.app](#railwayapp)
   - [DigitalOcean](#digitalocean)
   - [AWS](#aws)
   - [Google Cloud Platform](#google-cloud-platform)
4. [Environment Variables](#environment-variables)
5. [Database Persistence](#database-persistence)
6. [Troubleshooting](#troubleshooting)
7. [Production Best Practices](#production-best-practices)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ Docker and Docker Compose installed
- ✅ A Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- ✅ Git installed
- ✅ A cloud provider account (Render, Railway, DigitalOcean, AWS, or GCP)

---

## Local Docker Deployment

### Step 1: Clone and Navigate

```bash
cd your-own-knowledge-copilot
```

### Step 2: Set Environment Variables

Create a `.env` file in the root directory:

```bash
# Backend .env
cd backend
cat > .env << EOF
GEMINI_API_KEY=your_actual_gemini_api_key_here
DATABASE_URL=sqlite:///./knowledge_copilot.db
CHROMA_PERSIST_DIRECTORY=./chroma_db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
EOF
cd ..
```

### Step 3: Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Cloud Deployment Options

### Render.com

Render is excellent for quick deployments with automatic SSL.

#### Backend Deployment

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `knowledge-copilot-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Docker`
     - **Dockerfile Path**: `backend/Dockerfile`
     - **Plan**: Choose based on your needs

3. **Set Environment Variables**
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ALLOWED_ORIGINS=https://your-frontend-domain.onrender.com
   DATABASE_URL=sqlite:///./knowledge_copilot.db
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   ```

4. **Add Persistent Disk** (Important for data persistence)
   - In Render dashboard, go to your service
   - Add a Persistent Disk
   - Mount path: `/app/chroma_db` and `/app/knowledge_copilot.db`

5. **Deploy!**

#### Frontend Deployment

1. **Build Frontend Locally First** (to test)
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Create Static Site on Render**
   - "New +" → "Static Site"
   - Connect repository
   - Configure:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`
     - **Environment Variable**:
       ```
       VITE_API_URL=https://your-backend-service.onrender.com
       ```

**Using render.yaml (Alternative)**

You can also use the existing `render.yaml`:

```bash
# Update render.yaml with your settings
# Then deploy via Render CLI or dashboard
```

---

### Railway.app

Railway provides excellent Docker support with automatic deployments.

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   ```

3. **Deploy Backend**
   ```bash
   cd backend
   railway up
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set GEMINI_API_KEY=your_key
   railway variables set ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

5. **Deploy Frontend**
   - Create separate service for frontend
   - Set `VITE_API_URL` to your backend URL
   - Build command: `npm run build`
   - Start command: `npx serve -s dist -l 3000`

---

### DigitalOcean

#### Using App Platform

1. **Connect GitHub Repository**
   - Go to DigitalOcean App Platform
   - Create new app from GitHub

2. **Configure Backend Service**
   - Type: Web Service
   - Source: `backend` directory
   - Dockerfile: `backend/Dockerfile`
   - Environment Variables:
     ```
     GEMINI_API_KEY=your_key
     ALLOWED_ORIGINS=https://your-frontend-app.ondigitalocean.app
     ```

3. **Configure Frontend Service**
   - Type: Static Site
   - Source: `frontend` directory
   - Build Command: `npm install && npm run build`
   - Output Directory: `dist`
   - Environment Variable:
     ```
     VITE_API_URL=https://your-backend-app.ondigitalocean.app
     ```

#### Using Droplets with Docker

1. **Create Droplet**
   - Choose Ubuntu 22.04
   - Add Docker one-click app or install manually

2. **SSH into Droplet**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Clone and Deploy**
   ```bash
   git clone <your-repo-url>
   cd your-own-knowledge-copilot
   
   # Install Docker Compose if needed
   apt-get update
   apt-get install docker-compose
   
   # Create .env file
   nano backend/.env
   # Add your environment variables
   
   # Deploy
   docker-compose up -d
   
   # Set up Nginx reverse proxy (optional)
   apt-get install nginx
   # Configure nginx to proxy to your containers
   ```

---

### AWS

#### Using ECS (Elastic Container Service)

1. **Build and Push Docker Images**
   ```bash
   # Install AWS CLI and configure
   aws configure
   
   # Create ECR repository
   aws ecr create-repository --repository-name knowledge-copilot-backend
   aws ecr create-repository --repository-name knowledge-copilot-frontend
   
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   
   # Build and push backend
   cd backend
   docker build -t knowledge-copilot-backend .
   docker tag knowledge-copilot-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/knowledge-copilot-backend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/knowledge-copilot-backend:latest
   ```

2. **Create ECS Task Definition**
   - Use AWS Console or CLI
   - Configure environment variables
   - Set up EFS for persistent storage (for ChromaDB)

3. **Deploy to ECS Service**
   - Create cluster
   - Create service from task definition
   - Configure load balancer

#### Using EC2 with Docker Compose

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Configure security groups (ports 22, 80, 443, 8000)

2. **Install Docker**
   ```bash
   ssh -i your-key.pem ubuntu@ec2-ip
   sudo apt-get update
   sudo apt-get install docker.io docker-compose -y
   sudo usermod -aG docker ubuntu
   # Log out and back in
   ```

3. **Deploy Application**
   ```bash
   git clone <your-repo>
   cd your-own-knowledge-copilot
   # Create .env files
   docker-compose up -d
   ```

4. **Set Up Nginx Reverse Proxy**
   ```bash
   sudo apt-get install nginx certbot python3-certbot-nginx
   # Configure nginx config files
   sudo certbot --nginx -d your-domain.com
   ```

---

### Google Cloud Platform

#### Using Cloud Run

1. **Install Google Cloud SDK**
   ```bash
   # Install gcloud CLI
   gcloud init
   ```

2. **Build and Deploy Backend**
   ```bash
   cd backend
   gcloud builds submit --tag gcr.io/PROJECT_ID/knowledge-copilot-backend
   gcloud run deploy knowledge-copilot-backend \
     --image gcr.io/PROJECT_ID/knowledge-copilot-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your_key
   ```

3. **Deploy Frontend**
   ```bash
   cd frontend
   npm run build
   gcloud app deploy app.yaml  # Create app.yaml first
   ```

---

## Environment Variables

### Backend (.env)

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
DATABASE_URL=sqlite:///./knowledge_copilot.db
CHROMA_PERSIST_DIRECTORY=./chroma_db
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
ENVIRONMENT=production
PORT=8000
HOST=0.0.0.0
```

### Frontend (.env)

```bash
# Required for production
VITE_API_URL=https://your-backend-domain.com
```

**Note**: In Vite, environment variables must be prefixed with `VITE_` to be exposed to the client.

---

## Database Persistence

### SQLite (Current Setup)

SQLite is fine for small to medium deployments. For production:

1. **Use Persistent Volumes**
   - Mount `./knowledge_copilot.db` to persistent storage
   - Mount `./chroma_db` to persistent storage

2. **Regular Backups**
   ```bash
   # Backup script
   #!/bin/bash
   cp knowledge_copilot.db backups/knowledge_copilot_$(date +%Y%m%d_%H%M%S).db
   tar -czf chroma_db_backup_$(date +%Y%m%d_%H%M%S).tar.gz chroma_db/
   ```

### PostgreSQL (Recommended for Production)

For production, consider migrating to PostgreSQL:

1. **Update requirements.txt**
   ```
   psycopg2-binary==2.9.9
   ```

2. **Update DATABASE_URL**
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

3. **Update database.py** (SQLAlchemy already supports PostgreSQL)

---

## Troubleshooting

### Issue: CORS Errors

**Solution**: Update `ALLOWED_ORIGINS` in backend `.env`:
```bash
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

### Issue: Database Not Persisting

**Solution**: Ensure volumes are properly mounted in docker-compose.yml or cloud platform storage settings.

### Issue: ChromaDB Errors

**Solution**: 
- Ensure `chroma_db` directory has write permissions
- Check disk space
- Verify persistent storage is mounted

### Issue: API Connection Failed

**Solution**:
- Verify `VITE_API_URL` in frontend environment variables
- Check backend is running and accessible
- Verify CORS settings
- Check firewall/security group settings

### Issue: File Upload Fails

**Solution**:
- Check file size limits
- Verify temp directory exists and has write permissions
- Check disk space

### Issue: Out of Memory

**Solution**:
- Reduce number of workers in Dockerfile CMD
- Upgrade server/container resources
- Consider using a smaller embedding model

---

## Production Best Practices

### 1. Security

- ✅ Use HTTPS (SSL certificates)
- ✅ Set strong environment variables
- ✅ Enable rate limiting (consider adding middleware)
- ✅ Validate file uploads (already implemented)
- ✅ Regular security updates
- ✅ Use secrets management (AWS Secrets Manager, etc.)

### 2. Monitoring

- ✅ Set up health checks (already in Dockerfile)
- ✅ Monitor logs: `docker-compose logs -f`
- ✅ Set up error tracking (Sentry, etc.)
- ✅ Monitor resource usage

### 3. Performance

- ✅ Use CDN for frontend assets
- ✅ Enable gzip compression (nginx config included)
- ✅ Consider Redis for caching
- ✅ Optimize Docker images (multi-stage builds)
- ✅ Use load balancer for multiple instances

### 4. Scalability

- ✅ Use managed databases (PostgreSQL, etc.)
- ✅ Consider container orchestration (Kubernetes)
- ✅ Use managed vector databases (Pinecone, Weaviate)
- ✅ Implement horizontal scaling

### 5. Backup Strategy

- ✅ Automated database backups
- ✅ Backup ChromaDB directory
- ✅ Version control all code
- ✅ Document all environment variables

---

## Quick Start Commands

```bash
# Local development
docker-compose up --build

# Production build
docker-compose -f docker-compose.yml up --build -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Clean restart
docker-compose down -v
docker-compose up --build -d

# Update and redeploy
git pull
docker-compose up --build -d
```

---

## Support & Resources

- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🐳 [Docker Documentation](https://docs.docker.com/)
- ☁️ [Render Documentation](https://render.com/docs)
- 🚂 [Railway Documentation](https://docs.railway.app/)

---

## Next Steps

After successful deployment:

1. ✅ Set up monitoring and alerts
2. ✅ Configure custom domain
3. ✅ Set up CI/CD pipeline
4. ✅ Implement backup strategy
5. ✅ Add authentication (if needed)
6. ✅ Scale based on usage

---

**Happy Deploying! 🚀**

If you encounter any issues, check the troubleshooting section or open an issue on GitHub.

