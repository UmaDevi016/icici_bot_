from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
import uvicorn
import os
from chatbot import ICICIInsuranceChatbot

# Initialize FastAPI app
app = FastAPI(title="ICICI Insurance Chatbot", version="1.0.0")

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize chatbot
chatbot = None

@app.on_event("startup")
async def startup_event():
    """Initialize chatbot on startup"""
    global chatbot
    try:
        print("Initializing ICICI Insurance Chatbot...")
        chatbot = ICICIInsuranceChatbot()
        print("Chatbot initialized successfully!")
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        print("Server will continue with degraded functionality")
        # Don't raise to allow server to start
        chatbot = None

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    status: str
    relevant_chunks: int = 0

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """Handle chat requests"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        # Generate session ID if not provided
        session_id = chat_request.session_id or str(uuid.uuid4())
        
        # Get response from chatbot
        result = chatbot.chat(chat_request.message, session_id)
        
        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            status=result["status"],
            relevant_chunks=result["relevant_chunks"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history for a session"""
    if not chatbot:
        raise HTTPException(status_code=500, detail="Chatbot not initialized")
    
    try:
        history = chatbot.get_conversation_history(session_id)
        return {"history": history, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    is_ready = chatbot is not None
    return {
        "status": "healthy" if is_ready else "degraded",
        "chatbot_ready": is_ready,
        "chunks_loaded": len(chatbot.chunks) if is_ready and hasattr(chatbot, 'chunks') else 0
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if chatbot:
        chatbot.cleanup_files()
        print("Cleanup completed")

if __name__ == "__main__":
    print("Starting ICICI Insurance Chatbot Server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
