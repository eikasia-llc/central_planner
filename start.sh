#!/bin/bash
# Startup script for running both Flask API and Streamlit app

# Find python interpreter
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD=python
else
    echo "Error: Python not found." >&2
    exit 1
fi

# Start Flask API in background
echo "Starting Flask API server on port 8502..."
$PYTHON_CMD ./src/api_server.py &
FLASK_PID=$!

# Give Flask a moment to start
sleep 2

# Start Streamlit in foreground
echo "Starting Streamlit app on port 8501..."
streamlit run ./src/app.py --server.port 8501 --server.address 0.0.0.0

# If Streamlit exits, kill Flask too
kill $FLASK_PID 2>/dev/null
