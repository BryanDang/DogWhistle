# 🎤 DogWhistle Live Recording Demo

## What This Is

A **live web app** that records audio directly in the browser and processes it with AI - perfect for your hackathon demo!

## 🚀 Quick Start (30 seconds)

### 1. Start the Server
```bash
cd DogWhistle
python3 app.py
```

### 2. Open in Browser
- **On Demo Laptop**: http://localhost:8000
- **On Any Phone/Tablet**: http://YOUR-LAPTOP-IP:8000

### 3. Demo Flow
1. Click the red microphone button
2. Have a 30-60 second conversation
3. Click stop (square button)
4. Watch AI process in real-time
5. See results in ~20 seconds

## 📱 Features

### Visual Elements:
- **Animated Logo** - Floating DogWhistle icon
- **Live Audio Visualizer** - Shows sound waves while recording
- **Recording Timer** - Professional touch
- **Beautiful Dark UI** - Looks like a real product

### Demo Capabilities:
- Records directly in browser (no app needed)
- Works on ANY device with Chrome/Safari
- Processes with same AI backend
- Downloads meeting report

## 🎭 Demo Script (2 minutes)

### Opening (20 sec)
"DogWhistle captures and analyzes conversations with AI. Let me show you live."

### Recording (40 sec)
*Click record button*
"Let's have a quick discussion about [topic]. Notice the real-time audio visualization."
*Have actual conversation with team/judges*
*Click stop*

### Processing (20 sec)
"Now OpenAI's Whisper transcribes the audio, then GPT-4 extracts insights..."
*Point to spinning animation*

### Results (40 sec)
"In seconds, we get:
- Executive summary
- Action items with priorities  
- Follow-up questions
- All downloadable as a text report"

## 💡 Key Talking Points

**During Recording:**
- "Works on any device with a browser"
- "No app installation needed"
- "Privacy-first design"

**During Processing:**
- "Uses state-of-the-art AI models"
- "Costs only $0.10 per meeting"
- "Can process any length conversation"

**Showing Results:**
- "Actionable insights, not just transcription"
- "Helps teams never miss important decisions"
- "Integrates with any workflow"

## 🔧 Technical Details (if asked)

- **Frontend**: Pure HTML/JS (no framework needed)
- **Recording**: Web Audio API
- **Backend**: FastAPI + OpenAI
- **Processing**: Whisper + GPT-4
- **Deployment**: Can scale to cloud instantly

## 🚨 Troubleshooting

**"Microphone permission denied"**
- Browser will ask for permission
- Must click "Allow"

**"Processing taking long"**
- Normal for first request (server warming up)
- Subsequent recordings are faster

**"Can't connect from phone"**
- Ensure on same WiFi
- Check firewall isn't blocking port 8000

## 📊 What Makes This Special

1. **Live Demo** - Not a video or mockup
2. **Real AI** - Actually processes speech
3. **Instant Results** - See the power of AI
4. **Works Anywhere** - Phone, tablet, laptop
5. **Professional UI** - Looks production-ready

---

**Demo URL**: http://localhost:8000
**Best Browser**: Chrome or Safari
**Ideal Recording**: 30-60 seconds
**Processing Time**: ~20-30 seconds