from PIL import Image
import numpy as np
import cv2


def binarize(image: Image.Image, method: str, intensity: float) -> Image.Image:
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    if method == "simple":
        threshold_value = int(127 * intensity)
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    elif method == "adaptive":
        block_size = max(3, int(11 * intensity))
        if block_size % 2 == 0:
            block_size += 1
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 2)
    elif method == "otsu":
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        binary = gray

    return Image.fromarray(binary).convert('RGB')
