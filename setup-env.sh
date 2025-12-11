#!/bin/bash

# Setup script for Knowledge Copilot environment variables

echo "🔧 Setting up Knowledge Copilot Environment"
echo "=========================================="
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
        exit 0
    fi
fi

# Get Gemini API Key
echo "Enter your Gemini API Key"
echo "Get it from: https://makersuite.google.com/app/apikey"
echo ""
read -p "GEMINI_API_KEY: " GEMINI_KEY

if [ -z "$GEMINI_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY cannot be empty!"
    exit 1
fi

# Create .env file
cat > .env << EOF
# Gemini AI API Key (Required)
GEMINI_API_KEY=${GEMINI_KEY}

# CORS Configuration (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80

# Frontend API URL
VITE_API_URL=http://localhost:8000
EOF

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "📋 Contents:"
echo "----------"
cat .env | grep -v "GEMINI_API_KEY=${GEMINI_KEY}" | sed "s/${GEMINI_KEY}/***hidden***/g"
echo "GEMINI_API_KEY=***hidden***"
echo ""
echo "Next steps:"
echo "1. Make sure Docker Desktop is running"
echo "2. Run: docker-compose up --build -d"
echo "3. Visit: http://localhost:3000"
echo ""

