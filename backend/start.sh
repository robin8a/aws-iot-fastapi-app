#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8001"
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
