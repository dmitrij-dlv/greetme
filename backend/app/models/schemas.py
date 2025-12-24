from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    theme: str = Field(..., description="Coloring page theme")
    age_group: str = Field(..., description="Target age group")


class GenerateResponse(BaseModel):
    status: str
    prompt: str
    pdf_url: str
    preview_base64: str
    filename: str
    message: Optional[str] = None
