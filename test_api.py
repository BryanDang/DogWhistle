"""
Test the DogWhistle API endpoints
"""
import requests
import time
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing DogWhistle API...")
    print("=" * 50)
    
    # 1. Test health check
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # 2. Upload audio file
    print("\n2. Uploading audio file...")
    with open("Sample meeting recording.m4a", "rb") as f:
        files = {"audio_file": ("meeting.m4a", f, "audio/mp4")}
        response = requests.post(f"{BASE_URL}/api/meetings/upload", files=files)
    
    if response.status_code != 200:
        print(f"   ❌ Error: {response.status_code} - {response.text}")
        return
    
    upload_data = response.json()
    meeting_id = upload_data["meeting_id"]
    print(f"   ✅ Upload successful!")
    print(f"   Meeting ID: {meeting_id}")
    print(f"   Status: {upload_data['status']}")
    
    # 3. Check processing status
    print("\n3. Checking processing status...")
    max_attempts = 60  # Wait up to 5 minutes
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.get(f"{BASE_URL}/api/meetings/{meeting_id}/status")
        status_data = response.json()
        
        status = status_data["status"]
        progress = status_data.get("progress", 0)
        
        print(f"   Status: {status} ({progress}%)", end="\r")
        
        if status == "completed":
            print(f"\n   ✅ Processing completed!")
            break
        elif status == "failed":
            print(f"\n   ❌ Processing failed: {status_data.get('message')}")
            return
        
        time.sleep(5)  # Check every 5 seconds
        attempt += 1
    
    # 4. Get results
    print("\n4. Getting results...")
    response = requests.get(f"{BASE_URL}/api/meetings/{meeting_id}/results")
    
    if response.status_code != 200:
        print(f"   ❌ Error getting results: {response.text}")
        return
    
    results = response.json()
    
    # Display results
    print("\n📊 RESULTS:")
    print("-" * 50)
    
    # Transcript info
    transcript_info = results["transcript"]
    print(f"\n📝 Transcript:")
    print(f"   Word count: {transcript_info['word_count']}")
    print(f"   Duration estimate: {transcript_info['duration_estimate']}")
    print(f"   Preview: {transcript_info['full_text'][:200]}...")
    
    # Analysis
    analysis = results["analysis"]
    print(f"\n💡 Summary:")
    print(f"   Brief: {analysis['summary']['brief']}")
    
    print(f"\n📋 Action Items: {len(analysis['action_items'])} found")
    for i, item in enumerate(analysis['action_items'], 1):
        print(f"   {i}. {item['task']} (Priority: {item['priority']})")
    
    print(f"\n❓ Follow-up Questions:")
    for i, q in enumerate(analysis['follow_up_questions'], 1):
        print(f"   {i}. {q}")
    
    print(f"\n🏷️ Topics: {', '.join(analysis['topics_discussed'])}")
    print(f"💭 Sentiment: {analysis['sentiment']}")
    print(f"📅 Meeting Type: {analysis['meeting_type']}")
    
    # 5. Test consent revocation
    print("\n\n5. Testing consent check...")
    response = requests.post(
        f"{BASE_URL}/api/meetings/{meeting_id}/consent-check",
        params={"consent_given": True}
    )
    print(f"   Response: {response.json()['message']}")
    
    print("\n✅ All API tests completed successfully!")

if __name__ == "__main__":
    test_api()