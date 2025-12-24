from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    theme: str = Field(..., description="Coloring page theme")
    age_group: str = Field(..., description="Target age group")


class GenerateResponse(BaseModel):
    prompt: str
    pdf_base64: str
    preview_base64: str
    filename: str
    message: Optional[str] = None
