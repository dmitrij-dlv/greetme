from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    theme: str = Field(..., description="Coloring page theme")
    age_group: str = Field(..., description="Target age group")


class GenerateResponse(BaseModel):
    status: str = Field(..., description="ok on success")
    prompt: str
    pdf_url: str
    preview_base64: str
    filename: str
    pdf_base64: Optional[str] = None
    message: Optional[str] = None
