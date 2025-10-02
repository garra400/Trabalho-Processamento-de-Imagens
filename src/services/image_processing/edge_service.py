from PIL import Image
import numpy as np
import cv2


def detect_edges(image: Image.Image, method: str, intensity: float) -> Image.Image:
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    if method == "canny":
        low_threshold = int(50 * intensity)
        high_threshold = int(150 * intensity)
        edges = cv2.Canny(gray, low_threshold, high_threshold)
    elif method == "sobel":
        ksize = max(3, int(3 * intensity))
        if ksize % 2 == 0:
            ksize += 1
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        edges = np.sqrt(sobelx**2 + sobely**2)
        edges = np.uint8(edges * intensity)
    elif method == "laplacian":
        ksize = max(3, int(3 * intensity))
        if ksize % 2 == 0:
            ksize += 1
        edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
        edges = np.uint8(np.absolute(edges) * intensity)
    else:
        edges = gray

    return Image.fromarray(edges).convert('RGB')
