from typing import Union, List, Dict, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """A single message in a conversation."""

    content: Union[str, Dict, List[Dict]]
    role: str


class TokenUsage(BaseModel):
    """Token usage statistics for a chat completion."""

    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    content: List[Message]
    respondInLanguage: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str
    role: str = "assistant"
    usage: TokenUsage
    model: str
    stop_reason: Optional[str] = None
    message_id: Optional[str] = None


class SummarizeResponse(BaseModel):
    """Response model for summarize endpoint."""

    summary: str
    source_type: str  # "url" or "text"
    source: Optional[str] = None  # URL if source_type is "url", otherwise None
    usage: TokenUsage  # Reuse existing TokenUsage model
    model: str
