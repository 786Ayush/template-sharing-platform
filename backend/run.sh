#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install -r requirements.txt

# Run the FastAPI server for deployment
PORT=${PORT:-8000}
echo "Starting FastAPI server on port $PORT"
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
