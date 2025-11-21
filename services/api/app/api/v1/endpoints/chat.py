from fastapi import APIRouter
from typing import Optional
import anthropic

# internal
from app.core.config import settings, anthropic_client
from app.core.prompts import build_chat_system_prompt
from app.core.exceptions import validate_llm_response, handle_llm_error
from app.models.chat_models import ChatRequest, ChatResponse

router = APIRouter()

llm_model = settings.claude_model
MAX_TOKENS = settings.max_tokens


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for conversational AI with Claude.

    Supports multi-turn conversations and single queries.

    Args:
        request: ChatRequest containing messages and optional language preference

    Returns:
        ChatResponse with Claude's response, token usage, and metadata
    """
    # optional language instruction
    language_instruction = None
    if request.respondInLanguage:
        language_instruction = f"Always respond in {request.respondInLanguage}"

    system_prompt = build_chat_system_prompt(language_instruction)

    # TODO: REDIS CHECK: Look for cached summary first
    #     cache_key = f"summary:{hash(request.content)}"
    #     cached = await cache.get(cache_key)
    #     if not cached:
    #         return {"error": "Call /summarize first"}

    # convert pydantic models to dicts for anthropic
    messages = [msg.model_dump() for msg in request.content]

    try:
        message = await anthropic_client.messages.create(
            model=llm_model,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=messages,
        )

        # Calculate total tokens
        total_tokens = message.usage.input_tokens + message.usage.output_tokens

        return ChatResponse(
            response=message.content[0].text,
            role=message.role,
            usage={
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "total_tokens": total_tokens,
            },
            model=message.model,
            stop_reason=message.stop_reason,
            message_id=message.id,
        )
    except (
        anthropic.AuthenticationError,
        anthropic.RateLimitError,
        anthropic.APIConnectionError,
        anthropic.APIStatusError,
    ) as e:
        handle_llm_error(e)
