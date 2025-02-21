#!/bin/bash

# Make sure we're in the project root directory
cd "$(dirname "$0")/.."

# Run the Streamlit app
streamlit run app/streamlit/app.py --server.port 8501 