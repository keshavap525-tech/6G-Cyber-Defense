from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.api.automation import router as automation_router
from backend.api.detection import router as detection_router
from backend.api.incidents import router as incidents_router
from backend.api.simulator import router as simulator_router
from backend.api.auth import router as auth_router

app = FastAPI(
    title="AI-Powered 6G Cyber Defense System",
    description="AI-powered cybersecurity platform for simulated 6G networks",
    version="1.0.0"
)

# API routes
app.include_router(automation_router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(detection_router, tags=["Detection"])
app.include_router(incidents_router, tags=["Incidents"])
app.include_router(simulator_router, tags=["6G Simulator"])


# Main dashboard
@app.get("/")
def root():
    return {
        "project": "AI-Powered 6G Cyber Defense System",
        "status": "running",
        "version": "1.0.0",
        "documentation": "/docs",
        "dashboard": "/dashboard"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/dashboard")
@app.get("/dashboard/")
def dashboard():
    return FileResponse("frontend/dashboard.html")


# Static frontend files
app.mount(
    "/dashboard/static",
    StaticFiles(directory="frontend"),
    name="dashboard-static"
)
