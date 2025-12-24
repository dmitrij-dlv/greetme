import cv2
import numpy as np
from PIL import Image


class ImageProcessingPipeline:
    def __init__(self, line_thickness: int = 2):
        self.line_thickness = line_thickness

    def to_line_art(self, image: Image.Image) -> Image.Image:
        """Convert a PIL image to bold, printable line art."""
        grayscale = image.convert("L")
        np_img = np.array(grayscale)

        # Edge detection and thresholding for crisp outlines.
        edges = cv2.adaptiveThreshold(
            np_img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21,
            10,
        )

        # Invert so outlines are black on white.
        inverted = 255 - edges

        # Dilate to thicken lines for printing.
        kernel = np.ones((self.line_thickness, self.line_thickness), np.uint8)
        thick_lines = cv2.dilate(inverted, kernel, iterations=1)

        # Ensure white background and binary mask.
        cleaned = cv2.threshold(thick_lines, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cleaned = 255 - cleaned  # white background

        return Image.fromarray(cleaned).convert("RGB")
