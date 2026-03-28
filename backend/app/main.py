from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Club Penguin Avatar Marketplace",
    version="1.0.0",
    description="A virtual avatar marketplace API",
)

# CORS — allows your React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We'll register routers here as we build each feature
# app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "club-penguin-marketplace"}