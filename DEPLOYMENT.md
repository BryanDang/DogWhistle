# DogWhistle AI Deployment Guide

## Quick Start (Local Development)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
export OPENAI_API_KEY="your-api-key-here"
# Or use the api_keys.txt file

# 3. Run the server
python app.py

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## iOS Integration Example

```swift
// Upload audio file
func uploadMeeting(audioData: Data) async throws -> String {
    let url = URL(string: "http://your-server:8000/api/meetings/upload")!
    
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    
    let boundary = UUID().uuidString
    request.setValue("multipart/form-data; boundary=\(boundary)", 
                     forHTTPHeaderField: "Content-Type")
    
    // Create multipart form data
    var body = Data()
    body.append("--\(boundary)\r\n")
    body.append("Content-Disposition: form-data; name=\"audio_file\"; filename=\"meeting.m4a\"\r\n")
    body.append("Content-Type: audio/mp4\r\n\r\n")
    body.append(audioData)
    body.append("\r\n--\(boundary)--\r\n")
    
    request.httpBody = body
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let response = try JSONDecoder().decode(UploadResponse.self, from: data)
    
    return response.meetingId
}

// Check status
func checkStatus(meetingId: String) async throws -> MeetingStatus {
    let url = URL(string: "http://your-server:8000/api/meetings/\(meetingId)/status")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(MeetingStatus.self, from: data)
}

// Get results
func getResults(meetingId: String) async throws -> MeetingResults {
    let url = URL(string: "http://your-server:8000/api/meetings/\(meetingId)/results")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(MeetingResults.self, from: data)
}
```

## Production Deployment Options

### Option 1: Deploy to Vercel (Simplest)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

### Option 2: Deploy to AWS Lambda

```bash
# Use serverless framework
npm install -g serverless
serverless deploy
```

### Option 3: Deploy to Google Cloud Run

```bash
# Build container
docker build -t dogwhistle-ai .

# Deploy
gcloud run deploy dogwhistle-ai \
  --image dogwhistle-ai \
  --platform managed \
  --region us-central1
```

### Option 4: Traditional VPS (DigitalOcean, Linode, etc.)

```bash
# SSH to server
ssh your-server

# Clone repo
git clone https://github.com/Adil-Jussupov/DogWhistle.git
cd DogWhistle

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with supervisor or systemd
sudo nano /etc/systemd/system/dogwhistle.service
```

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=sk-proj-your-key-here
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://user:pass@localhost/dogwhistle
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=dogwhistle-audio-files
```

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Set CORS origins properly
- [ ] Implement rate limiting
- [ ] Add authentication headers
- [ ] Encrypt audio files at rest
- [ ] Set up monitoring/logging
- [ ] Configure auto-scaling
- [ ] Set up backup strategy

## Monitoring

Consider adding:
- Sentry for error tracking
- CloudWatch/Datadog for metrics
- Uptime monitoring
- Cost alerts for OpenAI usage