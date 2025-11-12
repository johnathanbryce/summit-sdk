from typing import Union, List, Dict, Optional
from pydantic import BaseModel


class Content(BaseModel):
    content: Union[str, Dict, List[Dict]]
    role: str


class QueryRequest(BaseModel):
    content: List[Content]
    respondInLanguage: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
