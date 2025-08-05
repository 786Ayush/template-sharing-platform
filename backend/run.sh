#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=production
export BASE_URL=https://template-sharing-platform1.onrender.com
export FRONTEND_URL=https://template-sharing-platform-5jwm18epe-ayushs-projects-b553b367.vercel.app
export ALLOW_ALL_ORIGINS=false

# Run the FastAPI server for deployment
PORT=${PORT:-8000}
echo "Starting FastAPI server on port $PORT"
uvicorn app.main:app --host 0.0.0.0 --port $PORT
