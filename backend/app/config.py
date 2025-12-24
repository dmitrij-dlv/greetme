import os
from pathlib import Path

APP_NAME = "Coloring Page Generator"
MEDIA_ROOT = Path(__file__).resolve().parent.parent / "output"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

PROMPT_TEMPLATE = (
    "Black and white line art coloring page for children.\n"
    "Subject: {theme}\n"
    "Style: simple, cute, friendly\n"
    "Age group: {age_group}\n"
    "Clear bold outlines\n"
    "No shading, no gray tones\n"
    "Pure white background\n"
    "Printable coloring book style\n"
    "Centered composition"
)

IMAGE_GENERATION_TIMEOUT = 25  # seconds
PROCESSING_TIMEOUT = 20  # seconds

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-image-1")
OPENAI_IMAGE_SIZE = os.getenv("OPENAI_IMAGE_SIZE", "1024x1024")

ALLOWED_THEMES = ["animals", "vehicles", "fantasy", "alphabet"]
ALLOWED_AGE_GROUPS = ["3-4", "5-6", "7-8"]
