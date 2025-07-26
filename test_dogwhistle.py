"""
Quick test script to verify DogWhistle AI processing
"""
import asyncio
import os
from dogwhistle_ai_processor import DogWhistleProcessor

async def test_processing():
    # Read API key from file
    with open("api_keys.txt", "r") as f:
        api_key = f.read().strip().split("=")[1]
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Initialize processor
    processor = DogWhistleProcessor()
    
    # Test with the sample audio file
    audio_file = "Sample meeting recording.m4a"
    meeting_id = "test-meeting-001"
    
    print(f"Testing DogWhistle AI processor with: {audio_file}")
    print("=" * 50)
    
    try:
        # Process the meeting
        results = await processor.process_meeting(audio_file, meeting_id)
        
        # Display results
        print("\n📝 TRANSCRIPT:")
        print("-" * 30)
        print(results["transcript"]["full_text"][:500] + "..." if len(results["transcript"]["full_text"]) > 500 else results["transcript"]["full_text"])
        
        print(f"\n📊 ANALYSIS:")
        print("-" * 30)
        analysis = results["analysis"]
        
        print(f"\n💡 Summary (Brief): {analysis['summary']['brief']}")
        print(f"\n📋 Action Items: {len(analysis['action_items'])} found")
        for i, item in enumerate(analysis['action_items'][:3], 1):
            print(f"  {i}. {item['task']}")
        
        print(f"\n❓ Follow-up Questions:")
        for i, q in enumerate(analysis['follow_up_questions'][:3], 1):
            print(f"  {i}. {q}")
        
        print(f"\n✅ Processing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check that your OpenAI API key is valid")
        print("2. Ensure you have sufficient API credits")
        print("3. Check internet connection")

if __name__ == "__main__":
    asyncio.run(test_processing())