from PIL import Image
import numpy as np
import cv2


def convert_color(image: Image.Image, conversion_type: str, intensity: float | None = None, iterations: int | None = None) -> Image.Image:
    # Conversões determinísticas, sem impacto de intensidade/iterações
    if conversion_type == "grayscale":
        return image.convert('L').convert('RGB')
    elif conversion_type == "hsv":
        # Converter via OpenCV para garantir fidelidade
        cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
        return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_HSV2RGB))
    elif conversion_type == "lab":
        cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2LAB)
        return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_LAB2RGB))
    elif conversion_type == "invert":
        np_image = np.array(image)
        inverted = 255 - np_image
        return Image.fromarray(inverted)
    else:
        return image.copy()
