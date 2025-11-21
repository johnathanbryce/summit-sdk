from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# endpoints
from app.api.v1.endpoints import health, chat, summarize

app = FastAPI(
    title="Summit API",
    description="AI-powered web content query service",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# instantiate routes:
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(summarize.router, prefix="/api/v1", tags=["summarize"])


@app.get("/")
async def root():
    return {"message": "Welcome to Summit API"}
