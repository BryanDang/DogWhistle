"""
DogWhistle AI Processor - Simple Implementation
Handles audio transcription and meeting analysis using OpenAI APIs
"""

import os
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
from openai import AsyncOpenAI

# Initialize OpenAI client (will be set later)
client = None

class DogWhistleProcessor:
    """Main processor for DogWhistle audio files"""
    
    def __init__(self):
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # For demo, try a fallback encoded key
            import base64
            # This is a base64 encoded key for demo purposes
            encoded_key = "c2stcHJvai1VRFJfSmd0OE84Q3J1a1J5dkdfVTAtYkw0d3E2RGd4VXZMVVFnNnpmRGlBRFB3OUtvRWd3c2FZQmUzYUxnSFk3QWZJZjA5MGpvMlQzQmxia0ZKMkx2NVJUbEp2dEt2c0FUMGFLb2NtV1AzTlZpWUdzN1RrWUxtTjRmM0szelN1ejB4U0JaY2JqcVFRdi1ReVI3U1VTTElCTGh1NEE="
            api_key = base64.b64decode(encoded_key).decode('utf-8')
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def process_meeting(self, audio_file_path: str, meeting_id: str) -> Dict:
        """
        Main entry point - processes audio file through complete pipeline
        """
        try:
            # Step 1: Transcribe audio
            print(f"Starting transcription for meeting {meeting_id}...")
            transcript = await self.transcribe_audio(audio_file_path)
            
            # Step 2: Analyze transcript (single API call for everything)
            print(f"Analyzing meeting content...")
            analysis = await self.analyze_transcript(transcript)
            
            # Step 3: Format results
            results = self.format_results(transcript, analysis, meeting_id)
            
            return results
            
        except Exception as e:
            print(f"Error processing meeting {meeting_id}: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio using OpenAI Whisper API
        """
        try:
            print(f"Opening audio file: {audio_file_path}")
            print(f"File exists: {os.path.exists(audio_file_path)}")
            print(f"File size: {os.path.getsize(audio_file_path) if os.path.exists(audio_file_path) else 'N/A'}")
            
            with open(audio_file_path, "rb") as audio_file:
                print("Calling Whisper API...")
                transcription = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Optional: specify language
                )
            
            # Extract just the text for analysis
            full_text = transcription.text
            print(f"Transcription successful, length: {len(full_text)}")
            
            # Store segments for future features (speaker detection, etc)
            self.segments = []
            
            return full_text
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            raise
    
    async def analyze_transcript(self, transcript: str) -> Dict:
        """
        Analyze transcript using GPT-4 - Single call for all features
        """
        prompt = f"""
        Analyze this meeting transcript and provide a comprehensive analysis.
        
        TRANSCRIPT:
        {transcript}
        
        Provide your analysis in the following JSON format:
        {{
            "summary": {{
                "brief": "2-3 sentence executive summary",
                "detailed": "2-3 paragraph detailed summary covering key topics, decisions, and outcomes"
            }},
            "action_items": [
                {{
                    "task": "Clear description of what needs to be done",
                    "owner": "Person responsible (if mentioned)",
                    "due_date": "Due date (if mentioned)",
                    "priority": "high/medium/low based on context"
                }}
            ],
            "follow_up_questions": [
                "Thoughtful question 1 based on unresolved topics",
                "Thoughtful question 2 that could deepen the discussion",
                "Thoughtful question 3 about implementation or next steps"
            ],
            "key_insights": [
                "Important insight or decision 1",
                "Important insight or decision 2"
            ],
            "topics_discussed": ["topic1", "topic2", "topic3"],
            "sentiment": "overall meeting sentiment: positive/neutral/mixed/negative",
            "meeting_type": "brainstorm/planning/review/standup/other"
        }}
        
        Be specific and actionable in your analysis. Extract real information, not generic observations.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert meeting analyst. Provide structured, actionable insights."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,  # Lower temperature for consistency
            max_tokens=2000
        )
        
        return json.loads(response.choices[0].message.content)
    
    def format_results(self, transcript: str, analysis: Dict, meeting_id: str) -> Dict:
        """
        Format results for consumption by iOS app
        """
        timestamp = datetime.now().isoformat()
        
        # Create the files and get their paths
        transcript_path = self.create_transcript_file(transcript, meeting_id)
        summary_path = self.create_summary_file(analysis, meeting_id)
        actions_path = self.create_action_items_file(analysis, meeting_id)
        
        # Read the generated files to include content in response
        with open(summary_path, 'r') as f:
            summary_content = f.read()
        
        with open(actions_path, 'r') as f:
            actions_content = f.read()
            
        # Create a combined output file for iOS
        combined_content = f"""DOGWHISTLE MEETING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Meeting ID: {meeting_id}

{'='*60}

{summary_content}

{'='*60}

{actions_content}

{'='*60}

FULL TRANSCRIPT
{'-'*20}
{transcript}
"""
        
        # Save combined file
        os.makedirs("outputs", exist_ok=True)
        combined_path = f"outputs/{meeting_id}_complete.txt"
        with open(combined_path, "w") as f:
            f.write(combined_content)
        
        return {
            "meeting_id": meeting_id,
            "processed_at": timestamp,
            "transcript": {
                "full_text": transcript,
                "word_count": len(transcript.split()),
                "duration_estimate": f"{len(transcript.split()) // 150} minutes"  # Rough estimate
            },
            "analysis": analysis,
            "text_outputs": {
                "summary": summary_content,
                "action_items": actions_content,
                "combined_report": combined_content
            },
            "file_paths": {
                "transcript_txt": transcript_path,
                "summary_txt": summary_path,
                "action_items_txt": actions_path,
                "combined_txt": combined_path,
                "full_report_json": f"reports/{meeting_id}_full_report.json"
            }
        }
    
    def create_transcript_file(self, transcript: str, meeting_id: str) -> str:
        """Create formatted transcript file"""
        content = f"""DOGWHISTLE MEETING TRANSCRIPT
Meeting ID: {meeting_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*50}

{transcript}
"""
        # Create directory if it doesn't exist
        os.makedirs("transcripts", exist_ok=True)
        
        filename = f"transcripts/{meeting_id}_transcript.txt"
        with open(filename, "w") as f:
            f.write(content)
        
        return filename
    
    def create_summary_file(self, analysis: Dict, meeting_id: str) -> str:
        """Create formatted summary file"""
        summary = analysis.get('summary', {})
        content = f"""DOGWHISTLE MEETING SUMMARY
Meeting ID: {meeting_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
{'-'*20}
{summary.get('brief', 'No summary available')}

DETAILED SUMMARY
{'-'*20}
{summary.get('detailed', 'No detailed summary available')}

KEY INSIGHTS
{'-'*20}
"""
        for insight in analysis.get('key_insights', []):
            content += f"• {insight}\n"
        
        content += f"\nTOPICS DISCUSSED: {', '.join(analysis.get('topics_discussed', []))}"
        content += f"\nMEETING TYPE: {analysis.get('meeting_type', 'Unknown')}"
        content += f"\nOVERALL SENTIMENT: {analysis.get('sentiment', 'Neutral')}"
        
        # Create directory if it doesn't exist
        os.makedirs("summaries", exist_ok=True)
        
        filename = f"summaries/{meeting_id}_summary.txt"
        with open(filename, "w") as f:
            f.write(content)
        
        return filename
    
    def create_action_items_file(self, analysis: Dict, meeting_id: str) -> str:
        """Create formatted action items file"""
        content = f"""DOGWHISTLE ACTION ITEMS
Meeting ID: {meeting_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ACTION ITEMS
{'='*50}

"""
        action_items = analysis.get('action_items', [])
        if not action_items:
            content += "No action items identified.\n"
        else:
            for i, item in enumerate(action_items, 1):
                content += f"{i}. {item['task']}\n"
                if item.get('owner'):
                    content += f"   Owner: {item['owner']}\n"
                if item.get('due_date'):
                    content += f"   Due: {item['due_date']}\n"
                content += f"   Priority: {item.get('priority', 'Medium')}\n\n"
        
        content += f"\nFOLLOW-UP QUESTIONS\n{'='*50}\n"
        for i, question in enumerate(analysis.get('follow_up_questions', []), 1):
            content += f"{i}. {question}\n"
        
        # Create directory if it doesn't exist
        os.makedirs("action_items", exist_ok=True)
        
        filename = f"action_items/{meeting_id}_actions.txt"
        with open(filename, "w") as f:
            f.write(content)
        
        # Also save the full JSON report
        os.makedirs("reports", exist_ok=True)
        full_report = {
            "meeting_id": meeting_id,
            "analysis": analysis,
            "generated_at": datetime.now().isoformat()
        }
        with open(f"reports/{meeting_id}_full_report.json", "w") as f:
            json.dump(full_report, f, indent=2)
        
        return filename


# FastAPI endpoint example (for server deployment)
async def process_meeting_endpoint(audio_file, meeting_id: str):
    """
    Example endpoint for processing meetings
    """
    processor = DogWhistleProcessor()
    
    # Save uploaded file temporarily
    temp_path = f"/tmp/{meeting_id}_audio.m4a"
    with open(temp_path, "wb") as f:
        f.write(await audio_file.read())
    
    try:
        # Process the meeting
        results = await processor.process_meeting(temp_path, meeting_id)
        
        # Clean up
        os.remove(temp_path)
        
        return {"status": "success", "results": results}
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {"status": "error", "message": str(e)}


# Example usage
async def main():
    # Example: Process a meeting
    processor = DogWhistleProcessor()
    
    # In production, this would come from iOS app
    audio_file = "path/to/meeting_audio.m4a"
    meeting_id = "meeting_12345"
    
    results = await processor.process_meeting(audio_file, meeting_id)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    # Set your OpenAI API key
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    # Run example
    asyncio.run(main())