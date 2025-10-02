from PIL import Image
import numpy as np
import cv2


def apply_morphology(image: Image.Image, operation: str, intensity: float, iterations: int) -> Image.Image:
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    kernel_size = max(3, int(5 * intensity))
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    result = binary
    for _ in range(iterations):
        if operation == "erosion":
            result = cv2.erode(result, kernel, iterations=1)
        elif operation == "dilation":
            result = cv2.dilate(result, kernel, iterations=1)
        elif operation == "opening":
            result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
        elif operation == "closing":
            result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)

    return Image.fromarray(result).convert('RGB')
