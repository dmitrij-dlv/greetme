import random
import textwrap
from io import BytesIO
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

from app import config


class ImageGenerator:
    """Placeholder image generator.

    In production this would call an AI image model. For the MVP we
    synthesize a high-contrast drawing so the rest of the pipeline can run.
    """

    def __init__(self, width: int = 2480, height: int = 3508):
        self.width = width
        self.height = height

    def build_prompt(self, theme: str, age_group: str) -> str:
        return config.PROMPT_TEMPLATE.format(theme=theme, age_group=age_group)

    def generate_image(self, theme: str, age_group: str) -> Tuple[str, Image.Image]:
        prompt = self.build_prompt(theme, age_group)
        image = self._draw_placeholder(theme, age_group)
        return prompt, image

    def _draw_placeholder(self, theme: str, age_group: str) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), "white")
        draw = ImageDraw.Draw(img)

        # Simple friendly shapes to keep content safe and child-appropriate.
        shapes = [
            ("circle", (self.width * 0.2, self.height * 0.2, self.width * 0.4, self.height * 0.4)),
            ("rectangle", (self.width * 0.55, self.height * 0.2, self.width * 0.8, self.height * 0.45)),
            ("triangle", (self.width * 0.3, self.height * 0.6, self.width * 0.5, self.height * 0.85)),
        ]
        random.shuffle(shapes)

        for shape, coords in shapes:
            if shape == "circle":
                draw.ellipse(coords, outline="black", width=12)
            elif shape == "rectangle":
                draw.rectangle(coords, outline="black", width=12)
            elif shape == "triangle":
                x1, y1, x2, y2 = coords
                draw.polygon([(x1, y2), ((x1 + x2) / 2, y1), (x2, y2)], outline="black", width=12)

        label = f"{theme.title()} | Ages {age_group}"
        font = ImageFont.load_default()
        wrapped = textwrap.fill(label, width=30)
        text_width, text_height = draw.multiline_textsize(wrapped, font=font)
        draw.multiline_text(
            ((self.width - text_width) / 2, self.height * 0.05),
            wrapped,
            fill="black",
            font=font,
            align="center",
        )

        return img
