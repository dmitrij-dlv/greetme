from io import BytesIO
from typing import Tuple

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


class PDFGenerator:
    def __init__(self, dpi: int = 300):
        self.dpi = dpi
        self.page_width_px = int(8.27 * dpi)
        self.page_height_px = int(11.69 * dpi)

    def build_pdf(self, image: Image.Image, filename: str) -> Tuple[str, bytes]:
        resized = image.resize((self.page_width_px, self.page_height_px))
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        img_buffer = BytesIO()
        resized.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        reader = ImageReader(img_buffer)

        width_pt, height_pt = A4
        c.drawImage(reader, 0, 0, width=width_pt, height=height_pt)
        c.showPage()
        c.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()
        img_buffer.close()

        return filename, pdf_bytes
