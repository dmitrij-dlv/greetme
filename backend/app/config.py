from pathlib import Path

APP_NAME = "Coloring Page Generator"
MEDIA_ROOT = Path(__file__).resolve().parent.parent / "output"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

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

ALLOWED_THEMES = ["animals", "vehicles", "fantasy", "alphabet"]
ALLOWED_AGE_GROUPS = ["3-4", "5-6", "7-8"]
