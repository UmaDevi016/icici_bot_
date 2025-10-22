@echo off
echo Starting ICICI Insurance Chatbot Server...
echo.
echo The server will start on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause
