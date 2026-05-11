from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, events, registrations, teams, projects, evaluations

app = FastAPI(
    title="Hackathon Management API",
    description="API for managing hackathon events",
    version="1.0.0"
)

# CORS middleware - MUST be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(registrations.router, prefix="/registrations", tags=["registrations"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])

@app.get("/")
async def root():
    return {
        "message": "Hackathon Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
