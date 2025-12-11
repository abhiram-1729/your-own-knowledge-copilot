# 🐳 Local Docker Setup Guide

## Prerequisites

1. **Docker Desktop** must be installed and running
   - Download from: https://www.docker.com/products/docker-desktop
   - Make sure Docker Desktop is **running** (you should see the Docker icon in your menu bar)

2. **Gemini API Key**
   - Get it from: https://makersuite.google.com/app/apikey

---

## Quick Setup Steps

### Step 1: Start Docker Desktop

**On macOS:**
- Open Docker Desktop from Applications
- Wait for it to fully start (Docker icon in menu bar should be stable)
- Verify it's running:
  ```bash
  docker ps
  ```
  If this works without errors, Docker is running!

### Step 2: Create Environment File

Create a `.env` file in the root directory:

```bash
cd /Users/abhiramrangoon/Desktop/own/your-own-knowledge-copilot

# Create .env file
cat > .env << 'EOF'
# Gemini AI API Key (Required)
GEMINI_API_KEY=your_actual_gemini_api_key_here

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80

# Frontend API URL
VITE_API_URL=http://localhost:8000
EOF
```

**Important:** Replace `your_actual_gemini_api_key_here` with your actual Gemini API key!

Alternatively, manually create the file:

```bash
nano .env
# or
code .env
# or
open -e .env
```

Then paste:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80
VITE_API_URL=http://localhost:8000
```

### Step 3: Build and Run

```bash
# Make sure you're in the project root
cd /Users/abhiramrangoon/Desktop/own/your-own-knowledge-copilot

# Build and start containers
docker-compose up --build -d

# View logs
docker-compose logs -f
```

### Step 4: Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## Troubleshooting

### Error: "Cannot connect to the Docker daemon"

**Solution:**
1. Make sure Docker Desktop is installed
2. **Start Docker Desktop** (most common issue!)
3. Wait for it to fully initialize
4. Try again: `docker ps`

### Warning: "GEMINI_API_KEY variable is not set"

**Solution:**
1. Create `.env` file in project root (see Step 2 above)
2. Make sure it contains `GEMINI_API_KEY=your_actual_key`
3. Try again: `docker-compose up --build -d`

### Error: Port already in use

**Solution:**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill the process or change ports in docker-compose.yml
```

### Containers keep restarting

**Solution:**
```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend

# Common issues:
# - Missing GEMINI_API_KEY
# - Port conflicts
# - Build errors
```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down

# Remove volumes (deletes data!)
docker-compose down -v

# Rebuild from scratch
docker-compose up --build -d
```

---

## Useful Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f              # All services
docker-compose logs -f backend      # Backend only
docker-compose logs -f frontend     # Frontend only

# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh
```

---

## Verify Installation

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Check containers are up:**
   ```bash
   docker-compose ps
   ```
   Both `backend` and `frontend` should show "Up"

3. **Test backend:**
   ```bash
   curl http://localhost:8000/
   ```
   Should return: `{"message":"Personal Knowledge Copilot API is running"}`

4. **Open frontend:**
   - Go to http://localhost:3000
   - Should see the Knowledge Copilot UI

---

## Next Steps

Once everything is running:

1. ✅ Upload a test document (PDF, DOCX, TXT, etc.)
2. ✅ Ask a question about your document
3. ✅ Verify AI responses work correctly

If everything works locally, you're ready to deploy to the cloud! See `DEPLOYMENT.md` for cloud deployment options.

---

**Still having issues?** Check the logs: `docker-compose logs -f`

