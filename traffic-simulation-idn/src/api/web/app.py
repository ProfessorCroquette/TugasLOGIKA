"""REST API application using FastAPI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Traffic Simulation Indonesia API",
    description="REST API for traffic simulation and violation management",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Traffic Simulation Indonesia API"}


@app.get("/api/vehicles")
def list_vehicles():
    """List all vehicles"""
    return {"data": [], "total": 0}


@app.get("/api/violations")
def list_violations():
    """List all violations"""
    return {"data": [], "total": 0}


@app.get("/api/reports/daily")
def daily_report(date: str):
    """Generate daily report"""
    return {"report_type": "daily", "date": date, "data": {}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
