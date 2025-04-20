#!/bin/bash

# This script stops all running servers

echo "Stopping AWS IoT Core FastAPI Web Application"
echo "============================================="

# Find and kill backend server
BACKEND_PID=$(pgrep -f "uvicorn main:app")
if [ -n "$BACKEND_PID" ]; then
  echo "Stopping backend server (PID: $BACKEND_PID)..."
  kill $BACKEND_PID
  echo "✅ Backend server stopped"
else
  echo "No running backend server found"
fi

# Find and kill frontend server
FRONTEND_PID=$(pgrep -f "node.*next")
if [ -n "$FRONTEND_PID" ]; then
  echo "Stopping frontend server (PID: $FRONTEND_PID)..."
  kill $FRONTEND_PID
  echo "✅ Frontend server stopped"
else
  echo "No running frontend server found"
fi

echo -e "\nAll servers stopped"
