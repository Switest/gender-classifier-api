# 📘 Gender Classification API 🚀

## 🚀 Overview
This project is a FastAPI-based backend service that classifies the gender of a given name using the external Genderize API. It processes raw API data, applies business logic, and returns a structured and enriched response.

---

## 📌 Features
- Accepts a name via query parameter  
- Integrates with external API (Genderize.io)  
- Extracts and processes gender prediction data  
- Renames count → sample_size  
- Computes confidence score (is_confident)  
- Generates dynamic timestamp (processed_at)  
- Handles errors and edge cases properly  
- Supports CORS for cross-origin access  

---

## 🔗 API Endpoint
GET /api/classify?name={name}

Example:
http://127.0.0.1:8000/api/classify?name=john

---

## 📤 Success Response (200 OK)
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-15T12:00:00Z"
  }
}

---

## ❌ Error Responses

400 Bad Request
{
  "status": "error",
  "message": "Name query parameter is required"
}

422 Unprocessable Entity
{
  "status": "error",
  "message": "Name is not valid"
}

502 Bad Gateway
{
  "status": "error",
  "message": "Upstream API error"
}

Edge Case
{
  "status": "error",
  "message": "No prediction available for the provided name"
}

---

## 🧠 Business Logic

Field Mapping:
count → sample_size  

Confidence Rule:
probability ≥ 0.7 AND sample_size ≥ 100  

Timestamp:
UTC ISO 8601 format (generated per request)

---

## ⚙️ Tech Stack
- Python  
- FastAPI  
- httpx  
- Uvicorn  

---

## 📦 Installation & Setup

1. Clone repository
git clone https://github.com/your-username/gender-classifier-api.git  
cd gender-classifier-api  

2. Install dependencies
pip install -r requirements.txt  

3. Run server
uvicorn main:app --reload  

4. Open in browser
http://127.0.0.1:8000/api/classify?name=john  

---

## 🌐 CORS
CORS is enabled for all origins:
allow_origins = ["*"]

---

## 🧪 Testing Checklist
- Valid name returns prediction  
- Empty name handled  
- Missing parameter handled  
- Edge case handled  
- External API failure handled  
- CORS enabled  
- Proper response format  

---

## 🚀 Deployment
Recommended platforms: Railway, AWS EC2, Fly.io  

Start command:
uvicorn main:app --host 0.0.0.0 --port 8000  

---

## 👨‍💻 Author
Backend API project demonstrating API integration, data processing, and error handling.

---

## 📌 License
For educational and assessment purposes.