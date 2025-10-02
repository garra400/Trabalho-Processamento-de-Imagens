from PIL import Image
import numpy as np
import cv2


def convert_color(image: Image.Image, conversion_type: str, intensity: float, iterations: int) -> Image.Image:
    result_image = image.copy()
    for _ in range(iterations):
        if conversion_type == "grayscale":
            gray_image = result_image.convert('L').convert('RGB')
            if intensity < 1.0:
                result_image = Image.blend(result_image, gray_image, intensity)
            else:
                result_image = gray_image
        elif conversion_type == "hsv":
            result_image = result_image.convert('HSV').convert('RGB')
        elif conversion_type == "lab":
            cv_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_RGB2LAB)
            result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_LAB2RGB))
        elif conversion_type == "invert":
            np_image = np.array(result_image)
            inverted = 255 - np_image
            inverted_image = Image.fromarray(inverted)
            if intensity < 1.0:
                result_image = Image.blend(result_image, inverted_image, intensity)
            else:
                result_image = inverted_image
    return result_image
