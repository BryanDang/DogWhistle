# DogWhistle AI - Hackathon Demo Setup Guide

## Quick Demo Setup (5 minutes)

### Prerequisites
- Python 3.8+ installed
- OpenAI API key (already in `api_keys.txt`)
- 8GB RAM minimum

### Step 1: Install Dependencies
```bash
# Create virtual environment (keeps your system Python clean)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install only what we need for the demo
pip install fastapi uvicorn openai aiofiles python-multipart
```

### Step 2: Run the Server
```bash
# Start the API server
python app.py

# You'll see: "DogWhistle AI API started successfully!"
# Server runs at: http://localhost:8000
```

### Step 3: Test It Works
```bash
# In a new terminal, run the test
python test_api.py

# This uploads the sample audio and shows the AI analysis
```

## What This Does

Your audio file gets processed through two AI models:

1. **Whisper** (Speech-to-Text): Converts audio → text transcript
2. **GPT-4** (Analysis): Extracts meeting insights in one shot

### Example Output Structure
```json
{
  "transcript": {
    "full_text": "Complete conversation text...",
    "word_count": 625,
    "duration_estimate": "4 minutes"
  },
  "analysis": {
    "summary": {
      "brief": "2-sentence summary",
      "detailed": "Full paragraph with key points"
    },
    "action_items": [
      {"task": "Do X", "priority": "high"},
      {"task": "Research Y", "priority": "medium"}
    ],
    "follow_up_questions": [
      "What about Z?",
      "How will we handle Q?"
    ]
  }
}
```

## Demo Script for Judges

### 1. Show the Problem (30 seconds)
"Ever leave a meeting and forget what was discussed? DogWhistle captures conversations with consent and gives you AI-powered summaries."

### 2. Live Demo (2 minutes)
```bash
# Terminal 1: Show the server running
python app.py

# Terminal 2: Upload an audio file
curl -X POST -F "audio_file=@demo_meeting.m4a" \
  http://localhost:8000/api/meetings/upload

# Show the processing status
curl http://localhost:8000/api/meetings/{meeting_id}/status

# Display the results
curl http://localhost:8000/api/meetings/{meeting_id}/results | python -m json.tool
```

### 3. Show the iOS Integration (1 minute)
Open `http://localhost:8000/docs` to show the interactive API documentation.

## Common Issues & Fixes

### "OpenAI API key not found"
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
# Or ensure api_keys.txt exists
```

### "Port 8000 already in use"
```bash
# Kill the process using port 8000
lsof -i :8000  # Find the PID
kill -9 [PID]  # Replace [PID] with actual number
```

### "Module not found" errors
```bash
# Make sure you're in the virtual environment
which python  # Should show: .../venv/bin/python
# If not, run: source venv/bin/activate
```

## Architecture Overview

```
Audio File → FastAPI Server → OpenAI Whisper → Transcript
                           ↓
                        GPT-4 Analysis
                           ↓
                    JSON Response → iOS App
```

### Key Files
- `app.py` - REST API server (handles HTTP requests)
- `dogwhistle_ai_processor.py` - Core AI logic (calls OpenAI)
- `test_api.py` - Demo script showing full workflow

## Optimization Tips for Demo

1. **Pre-process a sample**: Have results ready to show if API is slow
2. **Use shorter audio**: 1-2 minute clips process faster
3. **Cache results**: Reuse meeting IDs to avoid re-processing

## Talking Points

- **Privacy-first**: Consent required from all participants
- **Single API call**: Efficient GPT-4 prompt extracts everything at once
- **Cost-effective**: ~$0.10 per meeting (hackathon sustainable)
- **Easy integration**: REST API works with any frontend

## Next Steps After Hackathon

1. Add real-time transcription (streaming)
2. Implement speaker diarization (who said what)
3. Deploy to cloud (AWS Lambda for scale)
4. Add authentication & user management

---

**Remember**: This is a prototype. Focus on demonstrating the core value proposition - turning conversations into actionable insights with AI.