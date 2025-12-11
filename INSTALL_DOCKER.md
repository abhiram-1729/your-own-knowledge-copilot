# 🐳 Install Docker Desktop for Mac

## Current Status
❌ **Docker is NOT installed on your system**

You need to install Docker Desktop before you can run `docker-compose`.

---

## Installation Steps

### Step 1: Download Docker Desktop

**Option A: Direct Download**
1. Visit: https://www.docker.com/products/docker-desktop
2. Click "Download for Mac"
3. Choose the version for your Mac:
   - **Apple Silicon (M1/M2/M3)**: Download "Mac with Apple chip"
   - **Intel Mac**: Download "Mac with Intel chip"

**Option B: Using Homebrew** (if you have Homebrew installed)
```bash
brew install --cask docker
```

**Option C: Open Download Page**
```bash
open https://www.docker.com/products/docker-desktop
```

### Step 2: Install Docker Desktop

1. **Open the downloaded `.dmg` file**
   - Usually in your Downloads folder: `Docker.dmg`

2. **Drag Docker to Applications**
   - Drag the Docker icon to the Applications folder

3. **Open Docker Desktop**
   - Go to Applications
   - Double-click "Docker"
   - Or use Spotlight: Press `Cmd + Space`, type "Docker", press Enter

### Step 3: Complete Setup

1. **First Launch:**
   - Docker Desktop will ask for system permissions
   - Click "OK" or "Allow" when prompted
   - Docker will start initializing (this may take a few minutes)

2. **Wait for Docker to Start:**
   - Look for the Docker whale icon in your menu bar (top right)
   - Wait until the icon stops animating
   - It should show "Docker Desktop is running"

3. **Optional: Create Account**
   - You can skip account creation for now
   - Docker Desktop works without an account

### Step 4: Verify Installation

Open a new terminal window and run:

```bash
# Check Docker version
docker --version

# Check Docker is running
docker ps

# Check Docker Compose version
docker-compose --version
```

If these commands work **without errors**, Docker is successfully installed! ✅

---

## Quick Verification

After installing, verify Docker works:

```bash
# Test Docker
docker run hello-world
```

You should see a "Hello from Docker!" message if everything is working.

---

## After Docker is Installed

Once Docker Desktop is running:

1. **Navigate to your project:**
   ```bash
   cd /Users/abhiramrangoon/Desktop/own/your-own-knowledge-copilot
   ```

2. **Create .env file** (if not already created):
   ```bash
   ./setup-env.sh
   ```
   Or manually create `.env` with your `GEMINI_API_KEY`

3. **Run docker-compose:**
   ```bash
   docker-compose up --build -d
   ```

4. **Access your app:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

---

## Troubleshooting Installation

### Issue: "Docker cannot be opened because it is from an unidentified developer"

**Solution:**
1. Right-click on Docker Desktop
2. Select "Open"
3. Click "Open" in the dialog

### Issue: Docker won't start

**Solution:**
1. Make sure you have enough disk space (Docker needs ~4GB)
2. Check System Preferences → Security & Privacy → Allow Docker
3. Restart your Mac
4. Try opening Docker Desktop again

### Issue: Docker icon not appearing in menu bar

**Solution:**
- Docker might still be initializing (wait 2-3 minutes)
- Check if Docker process is running: `pgrep -f Docker`
- Try restarting Docker Desktop

### Issue: "Cannot connect to Docker daemon"

**Solution:**
- Make sure Docker Desktop is **running** (not just installed)
- Check menu bar for Docker icon
- Restart Docker Desktop: Menu bar → Docker icon → Quit, then reopen

---

## System Requirements

- **macOS**: 10.15 or newer
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 4GB free space
- **Virtualization**: Enabled (usually enabled by default)

---

## Alternative: Install via Terminal

If you prefer terminal installation:

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop
open -a Docker
```

---

## Next Steps

After Docker is installed and running:

1. ✅ Verify with `docker ps` (should work without errors)
2. ✅ Set up `.env` file with your Gemini API key
3. ✅ Run `docker-compose up --build -d`
4. ✅ Visit http://localhost:3000

---

## Need Help?

- **Docker Documentation**: https://docs.docker.com/desktop/install/mac-install/
- **Docker Desktop Issues**: https://docs.docker.com/desktop/troubleshoot/
- **Check Docker Status**: Menu bar → Docker icon → Settings

---

**Once Docker is installed and running, come back and run:**
```bash
cd /Users/abhiramrangoon/Desktop/own/your-own-knowledge-copilot
docker-compose up --build -d
```

