from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import Database
from app.api import auth, assessment, fitness, workouts, progress, admin

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB and Initialize Firebase
    await Database.connect()
    from app.core.security import initialize_firebase
    initialize_firebase()
    yield
    # Shutdown: Disconnect from MongoDB
    await Database.disconnect()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(assessment.router, prefix=settings.API_V1_PREFIX, tags=["assessment"])
app.include_router(fitness.router, prefix=settings.API_V1_PREFIX, tags=["fitness"])
app.include_router(workouts.router, prefix=settings.API_V1_PREFIX, tags=["workouts"])
app.include_router(progress.router, prefix=settings.API_V1_PREFIX, tags=["progress"])
app.include_router(admin.router, prefix=settings.API_V1_PREFIX, tags=["admin"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
