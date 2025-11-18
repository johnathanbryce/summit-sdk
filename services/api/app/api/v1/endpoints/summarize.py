from fastapi import APIRouter
from typing import Optional

# internal
from app.core.config import settings, anthropic_client
from app.models.chat_models import ChatRequest, ChatResponse
from app.api.v1.services import SummarizeService

router = APIRouter()

llm_model = settings.claude_model
api_key = settings.anthropic_api_key

MAX_TOKENS = settings.max_tokens


# TODO: Setup Redis cache
# from app.core.cache import RedisCache
# cache_client = RedisCache(settings.redis_url)
cache_client = None  # No cache for now

# TODO - cache the following
# 1. scraped website content
# 2. llm summary result


@router.post("/summarize")
async def summarize(request):
    """
    Summarize content (URL or raw text).
    """
    service = SummarizeService(llm_model, cache_client)
    result = await service.process(request.content)
    return result
