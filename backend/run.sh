#!/bin/bash

# Navigate to backend directory
cd /Users/ayushgupta/Documents/tasks/ass_full_stack/template-sharing-platform/backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install -r requirements.txt

# Run the FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
