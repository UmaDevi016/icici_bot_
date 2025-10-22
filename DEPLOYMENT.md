# 🚀 Deployment Guide - ICICI Insurance Chatbot

This guide covers multiple deployment options for your chatbot application.

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:
- ✅ All tests pass (`python test_dual_source.py`)
- ✅ Dependencies are listed in `requirements.txt`
- ✅ `.gitignore` excludes sensitive files
- ✅ Code is committed to Git
- ✅ You have the PDF file included

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Prerequisites
- Docker installed
- Docker Compose installed (optional)

### Build and Run

#### Using Docker Compose (Easiest)
```bash
docker-compose up -d
```

#### Using Docker Commands
```bash
# Build the image
docker build -t icici-chatbot .

# Run the container
docker run -d -p 8000:8000 --name icici-chatbot icici-chatbot
```

### Access
- Application: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Stop/Remove
```bash
docker-compose down
# OR
docker stop icici-chatbot
docker rm icici-chatbot
```

---

## ☁️ Option 2: Cloud Platforms

### A. Render (Free Tier Available)

1. **Create Account**: https://render.com

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: icici-insurance-chatbot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free

3. **Environment Variables** (if needed):
   - Add any custom variables

4. **Deploy**: Click "Create Web Service"

5. **Access**: Your app will be at `https://your-app-name.onrender.com`

**Note**: First request may be slow (cold start on free tier).

---

### B. Railway (Easy Deployment)

1. **Create Account**: https://railway.app

2. **Deploy from GitHub**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

3. **Configuration**:
   - Railway automatically runs: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Or add `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Custom Domain** (Optional):
   - Go to Settings → Add custom domain

5. **Access**: Railway provides a URL automatically

---

### C. Heroku

1. **Prerequisites**:
   - Heroku account
   - Heroku CLI installed

2. **Create `Procfile`** (already created, see below)

3. **Deploy**:
```bash
heroku login
heroku create icici-insurance-chatbot
git push heroku main
heroku open
```

4. **Scale**:
```bash
heroku ps:scale web=1
```

---

### D. AWS EC2 (Full Control)

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 LTS
   - t2.micro (free tier) or larger
   - Open port 8000 in security group

2. **SSH to Instance**:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Setup**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/UmaDevi016/icici_bot_.git
cd icici_bot_

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with nohup (background)
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

4. **Setup as Service** (Optional):
Create `/etc/systemd/system/chatbot.service`:
```ini
[Unit]
Description=ICICI Insurance Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/icici_bot_
ExecStart=/home/ubuntu/icici_bot_/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable chatbot
sudo systemctl start chatbot
```

---

### E. Google Cloud Platform (GCP)

1. **Deploy to Cloud Run**:
```bash
gcloud run deploy icici-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

2. **Access**: GCP provides a URL

---

### F. Azure Web App

1. **Create Web App**:
   - Portal: Create Resource → Web App
   - Runtime: Python 3.11
   - Region: Choose nearest

2. **Deploy**:
   - Use GitHub Actions (auto-configured)
   - Or use Azure CLI:
```bash
az webapp up --name icici-chatbot --runtime "PYTHON:3.11"
```

---

## 🔧 Production Configuration

### Environment Variables

Create `.env` file (don't commit):
```env
# Optional configurations
MAX_PDF_CHUNKS=150
MAX_WEB_PAGES=10
USE_WEB_CONTENT=true
LOG_LEVEL=info
```

Update code to use:
```python
import os
from dotenv import load_dotenv

load_dotenv()

max_pdf_chunks = int(os.getenv('MAX_PDF_CHUNKS', 150))
```

---

## 📊 Performance Optimization

### 1. Use Gunicorn for Production
```bash
pip install gunicorn
```

Run with:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. Enable Caching
- Keep embeddings cached (`chunks.pkl`, `embeddings.pkl`)
- These are loaded once on startup

### 3. Resource Requirements
- **Minimum**: 1 GB RAM, 1 CPU
- **Recommended**: 2 GB RAM, 2 CPUs
- **Storage**: 2 GB (models + embeddings)

---

## 🔒 Security Considerations

### 1. HTTPS/SSL
- Use platform's built-in SSL (Render, Railway, etc.)
- Or use Nginx as reverse proxy with Let's Encrypt

### 2. Rate Limiting
Add to `main.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    # ... existing code
```

### 3. CORS Configuration
Already configured in FastAPI, but customize if needed:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 Monitoring

### Health Check Endpoint
Already available at `/health`

### Logging
Add structured logging:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🧪 Testing Deployment

### Test Endpoints
```bash
# Health check
curl https://your-app-url.com/health

# Chat test
curl -X POST https://your-app-url.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ICICI Insurance?", "session_id": "test123"}'
```

---

## 📝 Procfile (for Heroku/Railway)

Already created for you:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## ⚠️ Common Issues

### Issue 1: App crashes on startup
**Solution**: Check logs, ensure all dependencies installed

### Issue 2: Slow first request
**Normal**: Model loading takes time. Pre-generate embeddings.

### Issue 3: Out of memory
**Solution**: 
- Use smaller instance
- Reduce chunk count
- Disable web scraping temporarily

### Issue 4: PDF not found
**Ensure**: PDF is included in deployment, not in .gitignore

---

## ✅ Recommended: Render Deployment

**Why Render?**
- ✅ Free tier available
- ✅ Auto SSL certificate
- ✅ Easy GitHub integration
- ✅ Persistent disk option
- ✅ Auto-deploy on push

**Steps**:
1. Push code to GitHub
2. Connect Render to GitHub
3. Deploy with one click
4. Access your chatbot!

---

## 🎉 You're Ready to Deploy!

Choose your preferred platform and follow the guide above. Your chatbot is production-ready! 🚀

**Need help?** Check platform-specific documentation or community forums.
