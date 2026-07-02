"""
main.py

FastAPI Application server for ClaimPulse Enterprise Portal.
Serves REST API endpoints and static image assets.
"""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import auth_routes, claim_routes

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("claimpulse_api")

app = FastAPI(
    title="ClaimPulse Enterprise API",
    description="AI Visual Evidence & Claim Adjudication Engine",
    version="2.0.0"
)

# CORS configuration for React Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(auth_routes.router)
app.include_router(claim_routes.router)

# Mount static files for images from dataset directory
REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = REPO_ROOT / "dataset" / "images"
if IMAGES_DIR.exists():
    app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "ClaimPulse Enterprise API", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
