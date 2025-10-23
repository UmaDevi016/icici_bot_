# 🚀 Deploy to Render (FREE Hosting)

## Prerequisites
- GitHub account (free)
- Render account (free) - https://render.com

---

## Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
```bash
git init
git add .
git commit -m "Ready for deployment"
```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Name: `icici-insurance-chatbot`
   - Make it **Public** or **Private**
   - Click "Create repository"

3. **Push Your Code**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/icici-insurance-chatbot.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy on Render

1. **Sign Up/Login**: https://render.com

2. **Create New Web Service**:
   - Click **"New +"** → **"Web Service"**
   - Click **"Build and deploy from a Git repository"**
   - Click **"Connect account"** → Connect GitHub

3. **Select Repository**:
   - Find and select `icici-insurance-chatbot`
   - Click **"Connect"**

4. **Configure Web Service**:
   ```
   Name: icici-insurance-chatbot
   Region: Singapore (or closest to you)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. **Select Free Plan**:
   - Instance Type: **Free**
   - Click **"Create Web Service"**

6. **Wait for Deployment** (5-10 minutes):
   - Render will install dependencies
   - Start your application
   - Provide a public URL

7. **Access Your Chatbot**:
   - URL will be: `https://icici-insurance-chatbot.onrender.com`
   - Share this URL with anyone!

---

## ✅ Your Chatbot is Now Public!

**Free Tier Includes:**
- ✅ HTTPS/SSL certificate (secure)
- ✅ Automatic deployments on git push
- ✅ 750 hours/month free
- ✅ Custom domain support (optional)

**Limitations:**
- ⚠️ Sleeps after 15 min of inactivity (wakes up in ~30 seconds)
- ⚠️ 512 MB RAM (sufficient for this app)

---

## 🔄 Update Your App

To update your chatbot after making changes:

```bash
git add .
git commit -m "Updated chatbot"
git push origin main
```

Render will automatically redeploy! 🎉

---

## ⚠️ Important Notes

1. **Initial Load**: First request after sleep may take 30 seconds
2. **Keep Alive**: Use a service like UptimeRobot to ping your URL every 5 minutes
3. **Environment Variables**: Add any secrets in Render Dashboard → Environment

---

## 🆘 Troubleshooting

**Build Fails?**
- Check Build Logs in Render Dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

**App Crashes?**
- Check Application Logs
- Ensure all files are committed to Git
- Verify `ICICI_Insurance.pdf` is in repository

**Slow Performance?**
- Normal on free tier after sleep
- Consider upgrading to paid tier ($7/month) for always-on

---

## 🎉 Done!

Your ICICI Insurance Chatbot is now:
- ✅ Publicly accessible
- ✅ Secured with HTTPS
- ✅ Auto-updating on git push
- ✅ FREE to host!

Share your URL: `https://icici-insurance-chatbot.onrender.com`
