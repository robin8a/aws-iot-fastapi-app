#!/bin/bash

# This script tests the AWS IoT Core connection and topic subscription

echo "Testing AWS IoT Core FastAPI Web Application"
echo "============================================"

# Check if backend is running
echo "Checking if backend is running..."
if curl -s http://localhost:8001/status > /dev/null; then
  echo "✅ Backend is running"
else
  echo "❌ Backend is not running. Please start the backend first with:"
  echo "   cd backend && source venv/bin/activate && ./start.sh"
  exit 1
fi

# Test API endpoints
echo -e "\nTesting API endpoints..."
echo "GET /status:"
curl -s http://localhost:8001/status | jq || echo "Failed to get status"

# Test topic subscription
echo -e "\nTesting topic subscription..."
echo "POST /subscribe:"
curl -s -X POST http://localhost:8001/subscribe \
  -H "Content-Type: application/json" \
  -d '{"topic":"test/topic"}' | jq || echo "Failed to subscribe to topic"

# Test WebSocket connection
echo -e "\nTesting WebSocket connection..."
echo "This test requires wscat. Installing if not present..."
npm install -g wscat

echo "Connecting to WebSocket endpoint..."
echo "Press Ctrl+C after a few messages to exit"
wscat -c ws://localhost:8000/ws
