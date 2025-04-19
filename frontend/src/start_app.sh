#!/bin/bash

# This script starts both the backend and frontend servers for testing

echo "Starting AWS IoT Core FastAPI Web Application"
echo "============================================="

# Start the backend server in the background
echo "Starting FastAPI backend server..."
cd /Users/robinochoa/Documents/fast_api_ws/aws-iot-fastapi-app/backend
source fast_api_venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8001 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"
echo "Backend logs available at: /Users/robinochoa/Documents/fast_api_ws/aws-iot-fastapi-app/backend/backend.log"

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8001/status > /dev/null; then
  echo "✅ Backend is running"
else
  echo "❌ Backend failed to start. Check logs at: /Users/robinochoa/Documents/fast_api_ws/aws-iot-fastapi-app/backend/backend.log"
  exit 1
fi

# Start the frontend server in the background
echo -e "\nStarting Next.js frontend server..."
cd /Users/robinochoa/Documents/fast_api_ws/aws-iot-fastapi-app/frontend
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"
echo "Frontend logs available at: /Users/robinochoa/Documents/fast_api_ws/aws-iot-fastapi-app/frontend/frontend.log"

# Wait for frontend to be ready
echo "Waiting for frontend to be ready..."
sleep 10

echo -e "\n✅ Application is now running!"
echo "- Backend: http://localhost:8001"
echo "- Frontend: http://localhost:3000"
echo -e "\nTo stop the servers, run: kill $BACKEND_PID $FRONTEND_PID"
