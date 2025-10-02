from PIL import Image
import numpy as np
import cv2


def binarize(
    image: Image.Image,
    method: str,
    intensity: float,
    threshold_value: int | None = None,
    block_size: int | None = None,
    C: int = 2,
) -> Image.Image:
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    if method == "simple":
        th = threshold_value if threshold_value is not None else int(127 * intensity)
        _, binary = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)
    elif method == "adaptive":
        bs = block_size if block_size is not None else max(3, int(11 * intensity))
        if bs % 2 == 0:
            bs += 1
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, bs, C)
    elif method == "otsu":
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        binary = gray

    return Image.fromarray(binary).convert('RGB')
