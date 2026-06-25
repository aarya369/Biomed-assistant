from typing import List, Literal
from pydantic import BaseModel

class Citation(BaseModel):
    document_id: str
    page_number: int
    chunk_index: int

class RAGResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: Literal["low", "medium", "high"]
