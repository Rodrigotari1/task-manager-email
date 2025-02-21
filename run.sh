#!/bin/bash

# Kill any existing processes on ports 8002 and 8501
echo "Killing existing processes..."
lsof -ti:8002 | xargs kill -9 2>/dev/null
lsof -ti:8501 | xargs kill -9 2>/dev/null

# Start the FastAPI backend
echo "Starting FastAPI backend..."
uvicorn app.main:app --port 8002 --reload &

# Wait a bit for the backend to start
sleep 2

# Start the Streamlit frontend
echo "Starting Streamlit frontend..."
streamlit run app/streamlit/app.py --server.port 8501

# The script will keep running until you press Ctrl+C
# When Ctrl+C is pressed, kill all background processes
trap 'kill $(jobs -p)' EXIT 