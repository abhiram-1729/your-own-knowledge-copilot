# 🔧 Fix Docker Issues

## Current Issues Detected

1. ❌ **Docker daemon not running** - Docker Desktop needs to be started
2. ⚠️ **GEMINI_API_KEY not set** - Need to create `.env` file
3. ✅ **docker-compose.yml version warning** - Fixed (removed obsolete version)

---

## Step-by-Step Fix

### 1. Install/Start Docker Desktop

**If Docker Desktop is NOT installed:**

1. Download Docker Desktop for Mac:
   ```bash
   open https://www.docker.com/products/docker-desktop
   ```
   Or visit: https://www.docker.com/products/docker-desktop

2. Install the `.dmg` file
3. Drag Docker to Applications
4. Open Docker Desktop from Applications
5. Wait for it to start (whale icon in menu bar)

**If Docker Desktop IS installed but not running:**

1. Open Docker Desktop from Applications
2. Wait for it to fully start (whale icon should be stable, not animated)
3. Verify it's working:
   ```bash
   docker --version
   docker ps
   ```

---

### 2. Create .env File

Create a `.env` file in your project root:

```bash
cd /Users/abhiramrangoon/Desktop/own/your-own-knowledge-copilot

# Option 1: Using echo
cat > .env << 'EOF'
GEMINI_API_KEY=your_gemini_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80
VITE_API_URL=http://localhost:8000
EOF

# Option 2: Using nano (editor)
nano .env
# Paste the content below, then Ctrl+X, Y, Enter

# Option 3: Using VS Code
code .env
# Paste the content below and save
```

**Content for .env file:**
```
GEMINI_API_KEY=your_gemini_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80
VITE_API_URL=http://localhost:8000
```

**⚠️ IMPORTANT:** Replace `your_gemini_api_key_here` with your actual API key!
- Get your key from: https://makersuite.google.com/app/apikey
- It should look like: `AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567`

---

### 3. Verify Docker is Running

```bash
# Check Docker version
docker --version

# Check Docker daemon is running
docker ps

# If these work, Docker is ready!
```

---

### 4. Try Again

Once Docker is running and `.env` file is created:

```bash
cd /Users/abhiramrangoon/Desktop/own/your-own-knowledge-copilot

# Build and start
docker-compose up --build -d

# Watch logs
docker-compose logs -f
```

---

## Quick Verification Checklist

- [ ] Docker Desktop is installed
- [ ] Docker Desktop is running (whale icon in menu bar)
- [ ] `docker ps` command works
- [ ] `.env` file exists in project root
- [ ] `.env` file contains your actual `GEMINI_API_KEY`
- [ ] You're in the project root directory

---

## Common Errors & Solutions

### Error: "Cannot connect to the Docker daemon"

**Cause:** Docker Desktop is not running

**Solution:**
1. Open Docker Desktop application
2. Wait for it to fully start
3. Try `docker ps` to verify

### Error: "The 'GEMINI_API_KEY' variable is not set"

**Cause:** Missing or incorrect `.env` file

**Solution:**
1. Create `.env` file in project root
2. Add `GEMINI_API_KEY=your_actual_key`
3. Make sure file is named exactly `.env` (not `.env.txt`)

### Error: Port 8000 or 3000 already in use

**Solution:**
```bash
# Find what's using the port
lsof -i :8000
lsof -i :3000

# Kill the process or change ports in docker-compose.yml
```

---

## Still Stuck?

1. **Check Docker Desktop status:**
   - Menu bar → Docker icon → Should show "Docker Desktop is running"

2. **Check Docker logs:**
   ```bash
   docker-compose logs
   ```

3. **Reset everything:**
   ```bash
   docker-compose down -v
   docker-compose up --build -d
   ```

4. **Verify .env file:**
   ```bash
   cat .env
   # Should show your GEMINI_API_KEY (not "your_gemini_api_key_here")
   ```

---

## Next Steps After Fix

Once Docker is running and `.env` is set:

1. ✅ Run `docker-compose up --build -d`
2. ✅ Wait for build to complete
3. ✅ Visit http://localhost:3000 (frontend)
4. ✅ Visit http://localhost:8000/docs (API docs)
5. ✅ Test uploading a document

---

**Need help?** Check `SETUP_LOCAL.md` for more detailed instructions.

