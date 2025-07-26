# 🚀 Deploy DogWhistle Demo Online (5 Minutes)

## Option 1: Render.com (Easiest - Free)

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Add DogWhistle demo with ultrasonic pairing"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your `DogWhistle` repo
5. Use these settings:
   - **Name**: `dogwhistle-demo`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Add environment variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: (paste from api_keys.txt)
7. Click "Create Web Service"

### 3. Your URL (in ~5 minutes)
```
https://dogwhistle-demo.onrender.com
```

## Option 2: Railway.app (Better Uptime)

### 1. Quick Deploy
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your DogWhistle repository
5. Add environment variable for API key
6. Deploy!

### 2. Your URL
```
https://dogwhistle-demo.railway.app
```

## Option 3: Replit (Fastest - Online IDE)

### 1. Import to Replit
1. Go to [replit.com](https://replit.com)
2. Click "Create Repl"
3. Import from GitHub URL
4. Add API key in Secrets

### 2. Your URL
```
https://dogwhistle.yourusername.repl.co
```

## Option 4: ngrok (Immediate - From Your Laptop)

### 1. Install ngrok
```bash
# Mac
brew install ngrok

# Or download from ngrok.com
```

### 2. Run Your Server
```bash
# Terminal 1
cd DogWhistle
python app.py
```

### 3. Create Public URL
```bash
# Terminal 2
ngrok http 8000
```

### 4. Your URL (temporary)
```
https://abc123.ngrok.io
```

## 🎯 For Your Demo

### Best Option: **Render**
- Free tier works perfectly
- Stable URL you can share
- Auto-deploys when you push to GitHub

### Quick Test: **ngrok**
- Instant public URL
- Good for quick testing
- URL changes each time

## 📱 Testing Together

Once deployed:
1. You open: `https://dogwhistle-demo.onrender.com`
2. Cofounder opens same URL on their device
3. One person "Transmits"
4. Other person "Listens"
5. Devices pair via ultrasonic demo!

## 🚨 Important Notes

### For Ultrasonic Demo:
- Both devices need speakers/microphone
- Works best on laptops/phones with good speakers
- May need to allow microphone permissions
- 17 kHz is audible (high-pitched tone)

### For Recording Demo:
- After pairing, can record meetings
- Results appear on both devices
- Processes with real AI (costs ~$0.10/meeting)