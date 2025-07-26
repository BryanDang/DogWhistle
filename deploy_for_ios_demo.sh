#!/bin/bash
# DogWhistle AI Server - iOS Demo Deployment Script

echo "🚀 DogWhistle AI Server Setup for iOS Demo"
echo "=========================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install fastapi uvicorn openai aiofiles python-multipart httpx

# Check if API key exists
if [ ! -f "api_keys.txt" ]; then
    echo "❌ api_keys.txt not found!"
    echo "Please create api_keys.txt with: OPENAI_API_KEY=your-key-here"
    exit 1
fi

echo "✅ API key found"

# Get local IP address for iOS to connect
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
else
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}')
fi

echo ""
echo "📱 iOS App Configuration:"
echo "========================"
echo "API Base URL: http://$LOCAL_IP:8000"
echo ""
echo "Endpoints for iOS:"
echo "- Upload: POST http://$LOCAL_IP:8000/api/meetings/upload"
echo "- Status: GET http://$LOCAL_IP:8000/api/meetings/{id}/status"
echo "- Results: GET http://$LOCAL_IP:8000/api/meetings/{id}/results"
echo "- Download: GET http://$LOCAL_IP:8000/api/meetings/{id}/download"
echo ""

# Start server
echo "🔥 Starting DogWhistle AI Server..."
echo "Press Ctrl+C to stop"
echo ""

# Run on all interfaces so iOS can connect
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload