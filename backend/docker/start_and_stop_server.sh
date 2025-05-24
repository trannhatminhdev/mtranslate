#!/bin/bash
# Activate conda environment
source activate openvoice
# Install libmagic
RUN conda install --yes -c conda-forge libmagic --solver=classic
# Start the server
uvicorn openvoice.openvoice_server:app --host "0.0.0.0" --port 8000 &
# Get its PID
PID=$!
# Wait for 300 seconds  to allow some models to download
sleep 300
# Kill the process
kill $PID
