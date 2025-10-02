from dataclasses import dataclass
from PIL import Image
from typing import Optional


@dataclass
class ImageModel:
    """Modelo para armazenar imagem original e processada"""
    original: Optional[Image.Image] = None
    processed: Optional[Image.Image] = None
