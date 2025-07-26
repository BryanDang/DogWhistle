# Deploy DogWhistle to Render (5 Minutes)

## 📋 Prerequisites
- GitHub account (your code needs to be pushed)
- Render account (free at render.com)

## 🚀 Step-by-Step Deployment

### 1. Prepare for Deployment
First, create a file to tell Render how to run your app:

**Create `render.yaml`:**
```yaml
services:
  - type: web
    name: dogwhistle-ai
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: OPENAI_API_KEY
        sync: false  # You'll add this manually
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Add DogWhistle AI backend"
git push origin main
```

### 3. Deploy on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your `DogWhistle` repository
5. Fill in:
   - **Name**: `dogwhistle-ai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Choose **Free** instance type
7. Click "Create Web Service"

### 4. Add OpenAI API Key

1. Go to your service dashboard
2. Click "Environment" in left sidebar
3. Add environment variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `sk-proj-your-key-here` (from api_keys.txt)
4. Click "Save Changes"

### 5. Wait for Deploy
- Takes 2-5 minutes first time
- Watch the logs for any errors
- When you see "Application startup complete" it's ready!

### 6. Get Your URL
Your API is now live at:
```
https://dogwhistle-ai.onrender.com
```

## 🧪 Test Your Deployment

```bash
# Test health check
curl https://dogwhistle-ai.onrender.com/

# Test wake endpoint
curl https://dogwhistle-ai.onrender.com/wake
```

## 📱 Update iOS App

In your iOS code, update:
```swift
let API_BASE_URL = "https://dogwhistle-ai.onrender.com"
```

## ⚡ Demo Day Tips

### Morning of Demo:
1. Visit https://dogwhistle-ai.onrender.com/docs
2. Do a test upload
3. This wakes the server and keeps it ready

### During Demo:
- First demo wakes server (if sleeping)
- Subsequent demos are instant
- Show the API docs to judges (looks professional!)

## 🚨 Troubleshooting

**"First request is slow"**
- Normal - server is waking up
- Add "Connecting to AI..." in iOS app

**"Deploy failed"**
- Check logs in Render dashboard
- Usually missing dependency
- Make sure requirements.txt is complete

**"API key error"**
- Double-check environment variable is set
- No quotes around the key value

## 🎯 What to Show Judges

1. **Live Demo**: Upload real audio from iOS
2. **API Docs**: Show https://dogwhistle-ai.onrender.com/docs
3. **Architecture**: "Deployed on cloud, scales automatically"
4. **Cost**: "Only $0.10 per meeting processed"

Your server URL: **https://dogwhistle-ai.onrender.com**