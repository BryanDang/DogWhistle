# DogWhistle iOS Integration Guide

## 🚀 Quick Setup for iOS Demo

### 1. Server URLs
```swift
// For local testing (same WiFi)
let LOCAL_API_URL = "http://YOUR_MAC_IP:8000"  // Replace with actual IP

// For cloud (Render) - works anywhere
let CLOUD_API_URL = "https://dogwhistle.onrender.com"

// Use this in your app
let API_BASE_URL = CLOUD_API_URL  // or LOCAL_API_URL
```

### 2. Add Wake-Up on App Launch

**In AppDelegate.swift:**
```swift
import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(_ application: UIApplication, 
                    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Wake up server on app launch
        wakeUpDogWhistleServer()
        
        return true
    }
    
    private func wakeUpDogWhistleServer() {
        guard let url = URL(string: "\(API_BASE_URL)/wake") else { return }
        
        // Fire and forget - we don't need the response
        URLSession.shared.dataTask(with: url) { _, _, _ in
            print("✅ DogWhistle server wake-up sent")
        }.resume()
    }
}
```

### 3. API Service Class

**Create DogWhistleAPI.swift:**
```swift
import Foundation

class DogWhistleAPI {
    static let shared = DogWhistleAPI()
    private let baseURL = API_BASE_URL
    
    // Upload audio file
    func uploadAudio(_ audioData: Data, completion: @escaping (Result<String, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/api/meetings/upload")!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"audio_file\"; filename=\"recording.m4a\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: audio/mp4\r\n\r\n".data(using: .utf8)!)
        body.append(audioData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data,
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let meetingId = json["meeting_id"] as? String else {
                completion(.failure(APIError.invalidResponse))
                return
            }
            
            completion(.success(meetingId))
        }.resume()
    }
    
    // Check processing status
    func checkStatus(meetingId: String, completion: @escaping (Result<ProcessingStatus, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/api/meetings/\(meetingId)/status")!
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data,
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let status = json["status"] as? String else {
                completion(.failure(APIError.invalidResponse))
                return
            }
            
            let progress = json["progress"] as? Int ?? 0
            completion(.success(ProcessingStatus(status: status, progress: progress)))
        }.resume()
    }
    
    // Get results
    func getResults(meetingId: String, completion: @escaping (Result<MeetingResults, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/api/meetings/\(meetingId)/results")!
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else {
                completion(.failure(APIError.noData))
                return
            }
            
            do {
                let results = try JSONDecoder().decode(MeetingResults.self, from: data)
                completion(.success(results))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
    
    // Download text report
    func downloadReport(meetingId: String, completion: @escaping (Result<String, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/api/meetings/\(meetingId)/download")!
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data,
                  let text = String(data: data, encoding: .utf8) else {
                completion(.failure(APIError.noData))
                return
            }
            
            completion(.success(text))
        }.resume()
    }
}

// Data Models
struct ProcessingStatus {
    let status: String  // pending, processing, completed, failed
    let progress: Int   // 0-100
}

struct MeetingResults: Codable {
    let meeting_id: String
    let text_outputs: TextOutputs
    let analysis: Analysis
}

struct TextOutputs: Codable {
    let summary: String
    let action_items: String
    let combined_report: String
}

struct Analysis: Codable {
    let summary: Summary
    let action_items: [ActionItem]
    let follow_up_questions: [String]
}

struct Summary: Codable {
    let brief: String
    let detailed: String
}

struct ActionItem: Codable {
    let task: String
    let priority: String
}

enum APIError: Error {
    case invalidResponse
    case noData
}
```

### 4. Usage Example in View Controller

```swift
class RecordingViewController: UIViewController {
    
    @IBAction func uploadRecording() {
        // Show loading
        showLoading("Uploading audio...")
        
        // Upload audio
        DogWhistleAPI.shared.uploadAudio(audioData) { [weak self] result in
            switch result {
            case .success(let meetingId):
                self?.pollForResults(meetingId: meetingId)
            case .failure(let error):
                self?.showError("Upload failed: \(error)")
            }
        }
    }
    
    func pollForResults(meetingId: String) {
        Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { timer in
            DogWhistleAPI.shared.checkStatus(meetingId: meetingId) { [weak self] result in
                switch result {
                case .success(let status):
                    self?.updateProgress(status.progress)
                    
                    if status.status == "completed" {
                        timer.invalidate()
                        self?.fetchResults(meetingId: meetingId)
                    } else if status.status == "failed" {
                        timer.invalidate()
                        self?.showError("Processing failed")
                    }
                case .failure:
                    // Keep polling
                    break
                }
            }
        }
    }
    
    func fetchResults(meetingId: String) {
        DogWhistleAPI.shared.getResults(meetingId: meetingId) { [weak self] result in
            switch result {
            case .success(let results):
                self?.displayResults(results)
            case .failure(let error):
                self?.showError("Failed to get results: \(error)")
            }
        }
    }
    
    func displayResults(_ results: MeetingResults) {
        // Show the combined report in a text view
        resultTextView.text = results.text_outputs.combined_report
    }
}
```

## 📱 Demo Day Checklist

- [ ] Set `API_BASE_URL` to cloud URL
- [ ] Test on real device (not just simulator)
- [ ] Add error handling for no internet
- [ ] Pre-test 30 min before demo
- [ ] Have local server as backup

## 🚨 Troubleshooting

**"Connection refused"**
- Check WiFi connection
- Verify server URL is correct
- Make sure server is running

**"Slow response"**
- Normal on first request (server waking up)
- Subsequent requests will be fast

**"File too large"**
- Compress audio before upload
- Limit recordings to 5 minutes