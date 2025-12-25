import asyncio
import base64
import random
import textwrap
from io import BytesIO
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

from app import config


class ImageGenerator:
    """Image generator backed by OpenAI with a safe placeholder fallback."""

    def __init__(self, width: int = 2480, height: int = 3508):
        self.width = width
        self.height = height
        self.client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None

    def build_prompt(self, theme: str, age_group: str) -> str:
        return config.PROMPT_TEMPLATE.format(theme=theme, age_group=age_group)

    async def generate_image(self, theme: str, age_group: str) -> Tuple[str, Image.Image]:
        prompt = self.build_prompt(theme, age_group)
        if self.client:
            try:
                image = await asyncio.to_thread(self._generate_with_openai, prompt)
                return prompt, image
            except Exception:
                # Fallback to placeholder while still returning a usable asset.
                pass

        image = await asyncio.to_thread(self._draw_placeholder, theme, age_group)
        return prompt, image

    def _generate_with_openai(self, prompt: str) -> Image.Image:
        response = self.client.images.generate(
            model=config.OPENAI_MODEL,
            prompt=prompt,
            size="1024x1024",
            response_format="b64_json",
        )
        image_b64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_b64)
        return Image.open(BytesIO(image_bytes)).convert("RGB")

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
        # multiline_textsize was removed; multiline_textbbox provides the bounding box.
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.multiline_text(
            ((self.width - text_width) / 2, self.height * 0.05),
            wrapped,
            fill="black",
            font=font,
            align="center",
        )

        return img
