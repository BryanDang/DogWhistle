"""
DogWhistle AI Processing API
Simple REST API for iOS app integration
"""

import os
import uuid
import asyncio
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Optional
import aiofiles

from dogwhistle_ai_processor import DogWhistleProcessor

# Initialize FastAPI app
app = FastAPI(title="DogWhistle AI API", version="1.0.0")

# Add CORS for iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (use Redis/Database in production)
meeting_status = {}

# Response models
class MeetingUploadResponse(BaseModel):
    meeting_id: str
    status: str
    message: str

class MeetingStatusResponse(BaseModel):
    meeting_id: str
    status: str  # pending, processing, completed, failed
    progress: Optional[int] = None
    message: Optional[str] = None

class ProcessingError(BaseModel):
    error: str
    details: str

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize processor (will be done after API key is loaded)
processor = None

@app.get("/")
async def root():
    """Serve the ultrasonic demo interface"""
    return FileResponse("static/ultrasonic-demo.html")

@app.get("/api")
async def api_root():
    """Health check endpoint"""
    return {
        "service": "DogWhistle AI Processing API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/wake")
async def wake():
    """Wake endpoint for Render free tier - prevents cold starts"""
    return {
        "status": "awake",
        "message": "Server is ready",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/Sample meeting recording.m4a")
async def get_sample_audio():
    """Serve the sample audio file"""
    return FileResponse("Sample meeting recording.m4a", media_type="audio/mp4")

@app.post("/api/meetings/upload", response_model=MeetingUploadResponse)
async def upload_meeting(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
):
    """
    Upload audio file for processing
    iOS app sends audio file here
    """
    # Validate file
    if not audio_file.filename.endswith(('.mp3', '.m4a', '.wav', '.ogg', '.webm')):
        raise HTTPException(400, "Invalid audio format. Supported: mp3, m4a, wav, ogg, webm")
    
    # Check file size (25MB limit for OpenAI)
    contents = await audio_file.read()
    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(400, "File too large. Maximum size: 25MB")
    
    # Generate meeting ID
    meeting_id = str(uuid.uuid4())
    
    # Save file temporarily
    temp_path = f"/tmp/{meeting_id}_{audio_file.filename}"
    async with aiofiles.open(temp_path, 'wb') as f:
        await f.write(contents)
    
    # Update status
    meeting_status[meeting_id] = {
        "status": "pending",
        "progress": 0,
        "temp_path": temp_path
    }
    
    # Process in background
    background_tasks.add_task(process_meeting_async, meeting_id, temp_path)
    
    return MeetingUploadResponse(
        meeting_id=meeting_id,
        status="pending",
        message="Audio file uploaded successfully. Processing started."
    )

async def process_meeting_async(meeting_id: str, audio_path: str):
    """
    Background task to process meeting
    """
    try:
        # Update status
        meeting_status[meeting_id]["status"] = "processing"
        meeting_status[meeting_id]["progress"] = 20
        
        # Process with AI
        results = await processor.process_meeting(audio_path, meeting_id)
        
        # Store results
        meeting_status[meeting_id]["status"] = "completed"
        meeting_status[meeting_id]["progress"] = 100
        meeting_status[meeting_id]["results"] = results
        
        # Clean up temp file
        os.remove(audio_path)
        
    except Exception as e:
        meeting_status[meeting_id]["status"] = "failed"
        meeting_status[meeting_id]["error"] = str(e)
        
        # Clean up on error
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.get("/api/meetings/{meeting_id}/status", response_model=MeetingStatusResponse)
async def get_meeting_status(meeting_id: str):
    """
    Check processing status
    iOS app polls this endpoint
    """
    if meeting_id not in meeting_status:
        raise HTTPException(404, "Meeting not found")
    
    status_info = meeting_status[meeting_id]
    
    return MeetingStatusResponse(
        meeting_id=meeting_id,
        status=status_info["status"],
        progress=status_info.get("progress"),
        message=status_info.get("error") if status_info["status"] == "failed" else None
    )

@app.get("/api/meetings/{meeting_id}/results")
async def get_meeting_results(meeting_id: str):
    """
    Get processed results
    Returns transcript, summary, action items, and follow-up questions
    """
    if meeting_id not in meeting_status:
        raise HTTPException(404, "Meeting not found")
    
    status_info = meeting_status[meeting_id]
    
    if status_info["status"] != "completed":
        raise HTTPException(400, f"Meeting processing not completed. Status: {status_info['status']}")
    
    return status_info["results"]

@app.get("/api/meetings/{meeting_id}/download")
async def download_meeting_report(meeting_id: str):
    """
    Download the complete meeting report as a text file
    Perfect for iOS app to save/display
    """
    from fastapi.responses import PlainTextResponse
    
    if meeting_id not in meeting_status:
        raise HTTPException(404, "Meeting not found")
    
    status_info = meeting_status[meeting_id]
    
    if status_info["status"] != "completed":
        raise HTTPException(400, f"Meeting processing not completed. Status: {status_info['status']}")
    
    # Get the combined report text
    combined_report = status_info["results"]["text_outputs"]["combined_report"]
    
    # Return as downloadable text file
    return PlainTextResponse(
        content=combined_report,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=dogwhistle_{meeting_id}.txt"
        }
    )

@app.delete("/api/meetings/{meeting_id}")
async def delete_meeting(meeting_id: str):
    """
    Handle consent revocation
    Deletes all meeting data
    """
    if meeting_id not in meeting_status:
        raise HTTPException(404, "Meeting not found")
    
    # Delete from storage
    del meeting_status[meeting_id]
    
    # In production: Also delete from S3, database, etc.
    
    return {"message": "Meeting data deleted successfully"}

@app.post("/api/meetings/{meeting_id}/consent-check")
async def consent_check(meeting_id: str, consent_given: bool):
    """
    Post-meeting consent verification
    Part of DogWhistle's privacy-first approach
    """
    if meeting_id not in meeting_status:
        raise HTTPException(404, "Meeting not found")
    
    if not consent_given:
        # Delete all data if consent not given
        del meeting_status[meeting_id]
        return {"message": "Meeting data deleted per user request"}
    
    # Mark as consented
    meeting_status[meeting_id]["consented"] = True
    return {"message": "Consent recorded"}

# Load API key and initialize processor on startup
@app.on_event("startup")
async def startup_event():
    global processor
    # Load API key from file if not already set
    if not os.getenv("OPENAI_API_KEY"):
        try:
            with open("api_keys.txt", "r") as f:
                api_key = f.read().strip().split("=")[1]
            os.environ["OPENAI_API_KEY"] = api_key
        except Exception as e:
            print(f"Warning: Could not load API key from file: {e}")
    
    # Initialize processor
    processor = DogWhistleProcessor()
    print("✅ DogWhistle AI API started successfully!")

# For local development
if __name__ == "__main__":
    import uvicorn
    
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)