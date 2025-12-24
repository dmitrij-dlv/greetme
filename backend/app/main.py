import asyncio
from io import BytesIO
from typing import Tuple

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from app import config
from app.models.schemas import GenerateRequest, GenerateResponse
from app.services.image_generator import ImageGenerator
from app.services.image_processing import ImageProcessingPipeline
from app.services.pdf_generator import PDFGenerator
from app.services.rate_limiter import RateLimiter
from app.services.storage import StorageService

app = FastAPI(title=config.APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

image_generator = ImageGenerator()
pipeline = ImageProcessingPipeline()
pdf_generator = PDFGenerator()
storage = StorageService()
limiter = RateLimiter()

app.mount("/files", StaticFiles(directory=config.MEDIA_ROOT, html=False), name="files")


def validate_request(request: GenerateRequest) -> None:
    if request.theme not in config.ALLOWED_THEMES:
        raise HTTPException(status_code=400, detail="Unsupported theme")
    if request.age_group not in config.ALLOWED_AGE_GROUPS:
        raise HTTPException(status_code=400, detail="Unsupported age group")


async def run_with_timeout(coro, timeout: int, message: str):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError as exc:
        raise HTTPException(status_code=504, detail=message) from exc


def _image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


async def rate_limit_dependency(request: Request):
    allowed = await limiter.allow()
    if not allowed:
        raise HTTPException(status_code=429, detail="Too many requests, please slow down")
    return request


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, _=Depends(rate_limit_dependency)):
    validate_request(request)

    try:
        async def generate_image_task() -> Tuple[str, Image.Image]:
            return await asyncio.to_thread(
                image_generator.generate_image, request.theme, request.age_group
            )

        prompt, image = await run_with_timeout(
            generate_image_task(),
            config.IMAGE_GENERATION_TIMEOUT,
            "Image generation timed out",
        )

        async def processing_task() -> Image.Image:
            return await asyncio.to_thread(pipeline.to_line_art, image)

        processed_image = await run_with_timeout(
            processing_task(), config.PROCESSING_TIMEOUT, "Image processing timed out"
        )

        filename = storage.build_filename(request.theme)
        _, pdf_bytes = pdf_generator.build_pdf(processed_image, filename)
        preview_b64 = storage.to_base64(_image_to_bytes(processed_image))

        storage.save_pdf(filename, pdf_bytes)
        pdf_url = f"/files/{filename}"

        return GenerateResponse(
            status="ok",
            prompt=prompt,
            pdf_url=pdf_url,
            preview_base64=preview_b64,
            filename=filename,
            message="Coloring page generated successfully",
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Failed to generate coloring page") from exc


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})
