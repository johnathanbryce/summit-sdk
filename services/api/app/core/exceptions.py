from fastapi import HTTPException
import anthropic


def validate_llm_response(llm_response):
    if not llm_response.content or not llm_response.content[0].text.strip():
        raise HTTPException(
            status_code=502, detail="The LLM returned an empty response."
        )

    if llm_response.stop_reason == "max_tokens":
        raise HTTPException(
            status_code=502,
            detail="Max tokens reached - response was truncated",
        )


def handle_llm_error(e):
    """Convert Anthropic exceptions to HTTPExceptions."""

    if isinstance(e, anthropic.AuthenticationError):
        raise HTTPException(status_code=401, detail="Invalid API key.")
    elif isinstance(e, anthropic.RateLimitError):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    elif isinstance(e, anthropic.APIConnectionError):
        raise HTTPException(status_code=503, detail="Failed to connect to LLM service.")
    elif isinstance(e, anthropic.APIStatusError):
        raise HTTPException(status_code=502, detail=f"LLM service error: {e.message}")
    else:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")
