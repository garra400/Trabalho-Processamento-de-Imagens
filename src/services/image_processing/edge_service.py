from PIL import Image
import numpy as np
import cv2


def detect_edges(
    image: Image.Image,
    method: str,
    intensity: float,
    low_threshold: int | None = None,
    high_threshold: int | None = None,
    ksize: int | None = None,
) -> Image.Image:
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    if method == "canny":
        lt = low_threshold if low_threshold is not None else int(50 * intensity)
        ht = high_threshold if high_threshold is not None else int(150 * intensity)
        edges = cv2.Canny(gray, lt, ht)
    elif method == "sobel":
        k = ksize if ksize is not None else max(3, int(3 * intensity))
        if k % 2 == 0:
            k += 1
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=k)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=k)
        edges = np.sqrt(sobelx**2 + sobely**2)
        edges = np.uint8(edges * intensity)
    elif method == "laplacian":
        k = ksize if ksize is not None else max(3, int(3 * intensity))
        if k % 2 == 0:
            k += 1
        edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=k)
        edges = np.uint8(np.absolute(edges) * intensity)
    else:
        edges = gray

    return Image.fromarray(edges).convert('RGB')
