from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.health import router as health_router
from src.api.routers.companies import router as companies_router
from src.api.routers.screener import router as screener_router

# ----------------------------------------------------
# FastAPI Application
# ----------------------------------------------------
app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    description="REST API for Nifty100 Financial Intelligence Platform",
    version="1.0.0",
)

# ----------------------------------------------------
# CORS Configuration
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Register Routers
# ----------------------------------------------------
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    companies_router,
    prefix="/api/v1",
    tags=["Companies"],
)

app.include_router(
    screener_router,
    prefix="/api/v1",
    tags=["Screener"],
)

# ----------------------------------------------------
# Root Endpoint
# ----------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Nifty100 Financial Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
    }