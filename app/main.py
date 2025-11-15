"""Main application entry point for Gym Tracker API."""
from fastapi import FastAPI
from app.api.routes_webhook import router as webhook_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
  title="Gym Tracker API",
  description="API for tracking gym workouts and progress",
  version="1.0.0"
)

app.include_router(webhook_router)
