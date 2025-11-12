from fastapi import APIRouter
from typing import Optional

# internal
from app.core.config import settings, anthropic_client
from app.models.query_models import QueryRequest, QueryResponse

router = APIRouter()

llm_model = settings.claude_model
api_key = settings.anthropic_api_key

MAX_TOKENS = settings.max_tokens


def build_system_prompt(language_instruction: Optional[str]):
    system_prompt = f"""
        Your goal is to summarize whatever content you are provided as succinctly as possible while providing all critical facts, dates, and insights.
        You must provide the user with as much important content as possible while being terse so as not to overwhelm.
         
        {language_instruction}
        """
    return system_prompt


@router.post("/query", response_model=QueryResponse)
async def query_llm(request: QueryRequest):
    """
    Query endpoint that sends content to Claude for summarization.

    Args:
        request: QueryRequest containing messages and optional language preference

    Returns:
        QueryResponse with Claude's summary
    """

    # optional language instruction
    language_instruction = None
    if request.respondInLanguage:
        language_instruction = f"Always respond in {request.respondInLanguage}"

    system_prompt = build_system_prompt(language_instruction)

    # Convert Pydantic models to dicts for Anthropic API
    messages = [msg.model_dump() for msg in request.content]
    print(f"messages: {messages}")

    message = await anthropic_client.messages.create(
        model=llm_model,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=messages,
    )

    return QueryResponse(response=message.content[0].text)
