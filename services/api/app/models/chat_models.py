from typing import Union, List, Dict, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """A single message in a conversation."""

    content: Union[str, Dict, List[Dict]]
    role: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    content: List[Message]
    respondInLanguage: Optional[str] = None


class TokenUsage(BaseModel):
    """Token usage statistics for a chat completion."""

    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str
    role: str = "assistant"
    usage: TokenUsage
    model: str
    stop_reason: Optional[str] = None
    message_id: Optional[str] = None
