# DogWhistle AI Processing Architecture

## Overview
The AI processing backend receives audio files from the iOS app and processes them through OpenAI's APIs to deliver transcriptions, summaries, action items, and follow-up questions.

## High-Level Architecture

```
iOS App → API Gateway → Processing Queue → AI Services → Output Storage → iOS App
```

## Recommended Tech Stack

### Option 1: Serverless Architecture (Recommended)
- **API**: AWS API Gateway / Vercel Functions
- **Queue**: AWS SQS / Google Cloud Tasks
- **Processing**: AWS Lambda / Google Cloud Functions
- **Storage**: S3 / Google Cloud Storage
- **Database**: DynamoDB / Firestore

### Option 2: Simple Backend Server
- **Framework**: FastAPI (Python) or Express (Node.js)
- **Queue**: Redis + Bull Queue
- **Storage**: Local filesystem / S3
- **Database**: PostgreSQL / MongoDB

## API Endpoints

```
POST /api/meetings/upload
  - Receives audio file from iOS
  - Returns meeting_id for tracking

GET /api/meetings/{meeting_id}/status
  - Check processing status
  - Returns: pending | processing | completed | failed

GET /api/meetings/{meeting_id}/results
  - Get all processed outputs
  - Returns: transcript, summary, action_items, follow_up_questions

DELETE /api/meetings/{meeting_id}
  - Handle consent revocation
  - Deletes all associated data
```

## Processing Pipeline

### 1. Audio Receipt & Validation
```python
def receive_audio(file: UploadFile) -> str:
    # Validate file format (mp3, m4a, wav, etc.)
    # Check file size (OpenAI limit: 25MB)
    # Generate unique meeting_id
    # Store in temporary storage
    # Queue for processing
    return meeting_id
```

### 2. Transcription Service
```python
async def transcribe_audio(audio_path: str) -> dict:
    # Use OpenAI Whisper API
    # Handle long audio (chunk if needed)
    # Return transcript with timestamps
```

### 3. Meeting Analysis Service
```python
async def analyze_meeting(transcript: str) -> dict:
    # Single GPT-4 call with structured prompt
    return {
        "summary": "...",
        "action_items": [...],
        "follow_up_questions": [...],
        "key_insights": [...]
    }
```

### 4. Output Formatting
```python
def format_outputs(analysis: dict) -> dict:
    # Format for iOS app consumption
    # Create text file versions
    # Include metadata (processing time, participants, etc.)
```

## Simplified Pipeline (Elegant Solution)

### Single-Step Processing
Instead of multiple API calls, use one comprehensive prompt:

```python
MEETING_ANALYSIS_PROMPT = """
Analyze this meeting transcript and provide:

1. SUMMARY (2-3 paragraphs)
   - Key topics discussed
   - Main decisions made
   - Important insights

2. ACTION ITEMS
   - Task description
   - Assigned to (if mentioned)
   - Due date (if mentioned)

3. FOLLOW-UP QUESTIONS
   - 3-5 thoughtful questions to continue the conversation
   - Based on unresolved topics or areas needing clarification

4. KEY INSIGHTS
   - Notable quotes or ideas
   - Potential opportunities identified

Format as JSON for easy parsing.
"""
```

### Async Processing Pattern
```python
async def process_meeting(audio_file):
    # 1. Upload to storage & get URL
    audio_url = await upload_to_storage(audio_file)
    
    # 2. Start transcription (async)
    transcription_task = transcribe_audio_async(audio_url)
    
    # 3. Update status to "transcribing"
    update_meeting_status(meeting_id, "transcribing")
    
    # 4. Wait for transcription
    transcript = await transcription_task
    
    # 5. Analyze transcript
    update_meeting_status(meeting_id, "analyzing")
    analysis = await analyze_meeting(transcript)
    
    # 6. Store results
    await store_results(meeting_id, transcript, analysis)
    
    # 7. Notify iOS app (push notification or webhook)
    await notify_completion(meeting_id)
```

## Error Handling & Resilience

```python
@retry(max_attempts=3, backoff=exponential)
async def robust_api_call(func, *args, **kwargs):
    try:
        return await func(*args, **kwargs)
    except RateLimitError:
        await asyncio.sleep(60)  # Wait for rate limit reset
        raise
    except Exception as e:
        log_error(e)
        raise
```

## Cost Optimization

1. **Batch Processing**: Group multiple short meetings
2. **Caching**: Store common prompts/responses
3. **Smart Chunking**: For long meetings, process in segments
4. **Tiered Processing**: Quick summary first, detailed analysis on demand

## Security Considerations

1. **Audio Encryption**: Encrypt at rest and in transit
2. **API Key Management**: Use environment variables
3. **Access Control**: Validate user permissions
4. **Data Retention**: Auto-delete after consent period
5. **GDPR Compliance**: Right to deletion, data portability

## Deployment Strategy

### Development
```bash
# Local development
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Production
```bash
# Docker deployment
docker build -t dogwhistle-ai .
docker run -p 8000:8000 dogwhistle-ai

# Or serverless
serverless deploy
```

## Integration with iOS

### Request Format
```json
{
  "audio_file": "base64_encoded_audio",
  "metadata": {
    "participants": ["user1_id", "user2_id"],
    "duration": 1800,
    "timestamp": "2024-01-26T10:00:00Z"
  }
}
```

### Response Format
```json
{
  "meeting_id": "uuid",
  "status": "completed",
  "results": {
    "transcript_url": "https://...",
    "summary": "...",
    "action_items": [...],
    "follow_up_questions": [...],
    "processing_time": 45.2
  }
}
```

## Next Steps

1. Choose architecture (serverless vs server)
2. Set up development environment
3. Implement core transcription service
4. Add analysis capabilities
5. Create iOS integration endpoints
6. Deploy to staging
7. Test with real audio samples
8. Optimize for performance/cost