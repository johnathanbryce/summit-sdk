from fastapi import FastAPI

# endpoints
from app.api.v1.endpoints import health

app = FastAPI(
    title="Summit API",
    description="AI-powered web content query service",
    version="0.1.0",
)

# instantiate routes:
app.include_router(health.router, prefix="/api/v1", tags=["health"])


@app.get("/")
async def root():
    return {"message": "Welcome to Summit API"}
