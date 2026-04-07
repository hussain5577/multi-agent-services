# app/main.py
import uvicorn
from dotenv import load_dotenv

# CRITICAL: load_dotenv() must execute before anything imports app.services
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat_routes import router as chat_router

app = FastAPI(
    title="AION AI Module",
    description="Stateless Decision Engine for Instagram Commerce",
    version="1.0.0"
)

# Optional: Add CORS if you are testing from a browser-based tool
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the isolated routes to the app
app.include_router(chat_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "gemini-3-flash-preview"}

if __name__ == "__main__":
    # Start the server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)