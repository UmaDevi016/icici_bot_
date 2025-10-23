Write-Host "Starting ICICI Insurance Chatbot on http://localhost:8888...`n"
Write-Host "Press Ctrl+C to stop the server`n"

# Start the server on port 8888
python -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload
