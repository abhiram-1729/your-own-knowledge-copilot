#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Exception: {e}")
        return False

def setup_backend():
    """Setup the backend environment"""
    print("Setting up backend...")
    
    # Create virtual environment
    if not run_command("python3 -m venv venv"):
        return False
    
    # Install requirements
    pip_cmd = "venv/bin/pip" if sys.platform != "win32" else "venv\\Scripts\\pip"
    if not run_command(f"{pip_cmd} install -r requirements.txt", "backend"):
        return False
    
    print("Backend setup completed successfully!")
    return True

def setup_frontend():
    """Setup the frontend environment"""
    print("Setting up frontend...")
    
    # Install npm dependencies
    if not run_command("npm install", "frontend"):
        return False
    
    print("Frontend setup completed successfully!")
    return True

def main():
    print("Setting up Personal Knowledge Copilot...")
    
    # Setup backend
    if not setup_backend():
        print("Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("Frontend setup failed!")
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    print("1. Backend: cd backend && source venv/bin/activate && python main.py")
    print("2. Frontend: cd frontend && npm run dev")
    print("\nAccess the application at http://localhost:3000")

if __name__ == "__main__":
    main()