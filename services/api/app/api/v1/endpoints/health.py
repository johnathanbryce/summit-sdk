from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health Check",
    description="Returns the current health status of the API",
    response_description="Service health status",
)
async def health():
    """Check if the API is running and healthy"""
    return {"status": "ok"}
