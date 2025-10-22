# 🚀 Quick Start Guide - ICICI Insurance Chatbot

## Your Chatbot is Ready! ✅

The server is currently **RUNNING** at: **http://localhost:8000**

---

## 📖 How to Use

### Step 1: Open the Application

Click here or paste in your browser: **http://localhost:8000**

### Step 2: Start Chatting

Type any question about ICICI Insurance in the chat box and press Enter!

### Example Questions to Try:

1. **"What is ICICI Insurance?"**
   - Get an overview of the company

2. **"What types of insurance do you offer?"**
   - Learn about available products

3. **"How can I file a claim?"**
   - Get claim filing instructions

4. **"What are the premium payment options?"**
   - Understand payment methods

5. **"Tell me about life insurance plans"**
   - Explore life insurance offerings

---

## 🎯 Features You Can Use

### 💬 Natural Conversations
- Ask follow-up questions
- The bot remembers your conversation context
- Get specific, relevant answers from the PDF

### 🔄 Session Management
- Each browser session gets a unique ID
- Your conversation history is saved
- Refresh the page to start a new conversation

### ⚡ Quick Suggestions
- Click the suggestion buttons for quick queries
- They auto-fill common questions

---

## 🛠️ Managing the Server

### To Stop the Server:
- Press `Ctrl + C` in the terminal/command prompt
- Or close the terminal window

### To Restart the Server:
- Double-click `start_server.bat`
- Or run: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`

### To Check if Server is Running:
- Visit: http://localhost:8000/health
- Should see: `{"status":"healthy","chatbot_ready":true,"chunks_loaded":200}`

---

## 📊 What's Happening Behind the Scenes?

1. **Your Question** → Converted to vector embedding
2. **Search** → Finds top 5 most relevant chunks from 200 PDF chunks
3. **Context** → Includes your previous 3-5 messages
4. **Response** → Generates answer based on relevant content
5. **Storage** → Saves conversation in SQLite database

---

## 💡 Tips for Best Results

✅ **DO:**
- Ask specific questions about ICICI Insurance
- Use complete sentences
- Ask follow-up questions for more detail
- Try the quick suggestion buttons

❌ **DON'T:**
- Ask about other insurance companies
- Expect information not in the PDF
- Use very short or vague queries

---

## 🔍 Troubleshooting

### Problem: Can't access http://localhost:8000
**Solution:** 
- Check if server is running
- Run: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`

### Problem: Bot gives generic responses
**Solution:**
- Try rephrasing your question
- Be more specific about what you want to know
- Use keywords from ICICI Insurance context

### Problem: Slow responses
**Solution:**
- First query takes longer (loading model)
- Subsequent queries are fast (~1 second)
- This is normal behavior

---

## 📁 Important Files

- **conversations.db** - Your chat history (can delete to clear history)
- **chunks.pkl** - 200 processed PDF chunks (don't delete)
- **embeddings.pkl** - Vector embeddings (don't delete)

---

## 🎓 Understanding the Technology

### RAG (Retrieval Augmented Generation)
The bot uses RAG to:
1. **Retrieve** relevant information from the PDF
2. **Augment** with conversation context
3. **Generate** accurate, contextual responses

### Vector Embeddings
Each PDF chunk is converted to a 384-dimensional vector that captures semantic meaning, enabling intelligent search.

### Cosine Similarity
Measures how similar your question is to each PDF chunk, returning the most relevant content.

---

## 🎉 You're All Set!

Your ICICI Insurance Chatbot is:
- ✅ Processing 200 PDF chunks
- ✅ Maintaining conversation context
- ✅ Storing chat history in database
- ✅ Running on FastAPI backend
- ✅ Serving a beautiful frontend

**Enjoy chatting with your AI assistant!** 🤖

---

## 📞 Technical Information

- **Server**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (FastAPI auto-generated)
- **Python Version**: 3.11.9
- **Framework**: FastAPI
- **ML Model**: all-MiniLM-L6-v2

---

**Need Help?** Check the full README.md or PROJECT_SUMMARY.md for detailed documentation.
