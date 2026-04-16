from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime

app = FastAPI()

# ✅ CORS (Required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 External API
GENDERIZE_URL = "https://api.genderize.io/"

# ✅ Optional root route (to avoid "Not Found")
@app.get("/")
def home():
    return {"message": "API is running"}

# ✅ Main Endpoint
@app.get("/api/classify")
async def classify_name(name: str = Query(...)):
    
    # 🔴 Validation: empty name
    if name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Name query parameter is required"}
        )

    try:
        # 🔵 Call external API
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name})

        # 🔴 Upstream error
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail={"status": "error", "message": "Upstream API error"}
            )

        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # 🔴 Edge case handling
        if gender is None or count == 0:
            return {
                "status": "error",
                "message": "No prediction available for the provided name"
            }

        # 🧠 Processing
        sample_size = count
        is_confident = probability >= 0.7 and sample_size >= 100

        return {
            "status": "success",
            "data": {
                "name": data.get("name"),
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": datetime.utcnow().isoformat() + "Z"
            }
        }

    except httpx.RequestError:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "Server or upstream error"}
        )

# ✅ Custom error handler (VERY IMPORTANT)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(exc.detail)
        }
    )
