import base64
from pathlib import Path
from typing import Tuple

from app import config


class StorageService:
    def __init__(self, root: Path = config.MEDIA_ROOT):
        self.root = root

    def save_pdf(self, filename: str, data: bytes) -> Path:
        path = self.root / filename
        path.write_bytes(data)
        return path

    @staticmethod
    def to_base64(data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def from_base64(data: str) -> bytes:
        return base64.b64decode(data.encode("utf-8"))

    def encode_file(self, path: Path) -> str:
        return self.to_base64(path.read_bytes())

    def build_filename(self, theme: str) -> str:
        safe_theme = theme.replace(" ", "_").lower()
        return f"coloring_{safe_theme}.pdf"
