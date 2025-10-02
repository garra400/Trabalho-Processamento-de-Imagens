from PIL import Image
from typing import Tuple


def create_preview(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    preview = image.copy()
    preview.thumbnail(max_size, Image.Resampling.LANCZOS)
    return preview
