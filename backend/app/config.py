import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Coloring Page Generator"
MEDIA_ROOT = Path(__file__).resolve().parent.parent / "output"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

# External services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-image-1")

PROMPT_TEMPLATE = (
    "Black and white line art coloring page for children.\n"
    "Subject: {theme}\n"
    "Style: simple, cute, friendly\n"
    "Age group: {age_group}\n"
    "Clear bold outlines, no shading, no gray tones\n"
    "White background, centered composition\n"
    "Printable coloring book style"
)

IMAGE_GENERATION_TIMEOUT = 20  # seconds
PROCESSING_TIMEOUT = 20  # seconds
RATE_LIMIT_REQUESTS = 30  # placeholder per-minute limit

ALLOWED_THEMES = ["animals", "vehicles", "fantasy", "alphabet"]
ALLOWED_AGE_GROUPS = ["3-4", "5-6", "7-8"]
