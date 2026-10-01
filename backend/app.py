from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# API routers
from backend.api.automation import router as automation_router
from backend.api.detection import router as detection_router
from backend.api.incidents import router as incidents_router
from backend.api.simulator import router as simulator_router

# Authentication router
from backend.api.auth import router as auth_router


# ============================================================
# CREATE FASTAPI APPLICATION FIRST
# ============================================================

app = FastAPI(
    title="AI-Powered 6G Cyber Defense System",
    description="AI-powered cybersecurity platform for simulated 6G networks",
    version="1.0.0"
)
# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTERS
# ============================================================
app.include_router(automation_router)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    detection_router,
    tags=["Detection"]
)

app.include_router(
    incidents_router,
    tags=["Incidents"]
)

app.include_router(
    simulator_router,
    tags=["6G Simulator"]
)


# ============================================================
# FRONTEND / DASHBOARD
# ============================================================

try:
    app.mount(
        "/dashboard",
        StaticFiles(
            directory="frontend",
            html=True
        ),
        name="dashboard"
    )
except RuntimeError:
    print("WARNING: frontend directory not found. Dashboard disabled.")


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "project": "AI-Powered 6G Cyber Defense System",
        "status": "running",
        "version": "1.0.0",
        "documentation": "/docs",
        "dashboard": "/dashboard/"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }