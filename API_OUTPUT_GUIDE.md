# DogWhistle API Output Guide

## 📍 Where to Find API Outputs

### 1. **API Documentation (Interactive)**
```
http://localhost:8000/docs
```
- Shows all endpoints with example responses
- You can test endpoints directly in the browser
- Click "Try it out" to see real responses

### 2. **File System Locations**
After processing a meeting, files are saved to:
```
DogWhistle/
├── outputs/
│   └── {meeting_id}_complete.txt      # Combined report for iOS
├── transcripts/
│   └── {meeting_id}_transcript.txt    # Full transcript
├── summaries/
│   └── {meeting_id}_summary.txt       # Summary only
├── action_items/
│   └── {meeting_id}_actions.txt       # Actions & questions
└── reports/
    └── {meeting_id}_full_report.json  # JSON format
```

## 📊 What the API Returns

### **POST /api/meetings/upload**
```json
{
  "meeting_id": "44463d23-a412-4586-891f-67a035727b7a",
  "status": "pending",
  "message": "Audio file uploaded successfully. Processing started."
}
```

### **GET /api/meetings/{meeting_id}/results**
```json
{
  "meeting_id": "44463d23-a412-4586-891f-67a035727b7a",
  "processed_at": "2025-07-26T13:12:22.609542",
  
  "transcript": {
    "full_text": "Okay, so let's describe this idea...",
    "word_count": 625,
    "duration_estimate": "4 minutes"
  },
  
  "analysis": {
    "summary": {
      "brief": "2-sentence executive summary",
      "detailed": "Full paragraph with context"
    },
    "action_items": [
      {
        "task": "Research existing apps",
        "owner": "Unspecified",
        "due_date": "Before next meeting",
        "priority": "high"
      }
    ],
    "follow_up_questions": [
      "What specific apps to target?",
      "How to ensure privacy?"
    ],
    "key_insights": [
      "App reduces friction for consent",
      "Monetization via paid conversations"
    ],
    "topics_discussed": ["AI consent", "Monetization"],
    "sentiment": "positive",
    "meeting_type": "brainstorm"
  },
  
  "text_outputs": {
    "summary": "DOGWHISTLE MEETING SUMMARY\n...",
    "action_items": "DOGWHISTLE ACTION ITEMS\n...",
    "combined_report": "DOGWHISTLE MEETING REPORT\n..."
  },
  
  "file_paths": {
    "combined_txt": "outputs/44463d23_complete.txt",
    "summary_txt": "summaries/44463d23_summary.txt",
    "action_items_txt": "action_items/44463d23_actions.txt"
  }
}
```

### **GET /api/meetings/{meeting_id}/download**
Returns plain text file:
```
DOGWHISTLE MEETING REPORT
Generated: 2025-07-26 13:31:05
Meeting ID: test-meeting-001

============================================================

EXECUTIVE SUMMARY
--------------------
The meeting focused on brainstorming an app...

ACTION ITEMS
--------------------
1. Research existing apps (Priority: high)
2. Explore monetization (Priority: medium)

FOLLOW-UP QUESTIONS
--------------------
1. What specific productivity apps?
2. How to ensure privacy?

FULL TRANSCRIPT
--------------------
[Complete conversation text...]
```

## 🧪 How to Test & View Outputs

### Method 1: Using curl (Terminal)
```bash
# Upload audio
curl -X POST -F "audio_file=@Sample meeting recording.m4a" \
  http://localhost:8000/api/meetings/upload

# Get results (replace with your meeting_id)
curl http://localhost:8000/api/meetings/{meeting_id}/results | python -m json.tool

# Download text file
curl http://localhost:8000/api/meetings/{meeting_id}/download -o meeting_report.txt
```

### Method 2: Using the Test Script
```bash
python test_api.py
# This will show all outputs in the terminal
```

### Method 3: Direct File Access
```bash
# View the generated text file
cat outputs/test-meeting-001_complete.txt

# View JSON report
cat reports/test-meeting-001_full_report.json | python -m json.tool
```

## 📱 iOS App Integration

Your iOS developer should use these endpoints:

1. **Upload Audio**: `POST /api/meetings/upload`
2. **Check Status**: `GET /api/meetings/{id}/status`
3. **Get Results**: `GET /api/meetings/{id}/results`
   - Use `text_outputs.combined_report` for display
4. **Download File**: `GET /api/meetings/{id}/download`
   - Save to device or share

The `combined_report` text is formatted for direct display in the iOS app.