from PIL import Image, ImageFilter


def apply_filter(
    image: Image.Image,
    filter_type: str,
    intensity: float,
    iterations: int,
    radius: int | None = None,
) -> Image.Image:
    result_image = image.copy()
    for _ in range(iterations):
        if filter_type == "blur":
            r = radius if radius is not None else max(1, int(intensity * 2))
            filtered_image = result_image.filter(ImageFilter.GaussianBlur(radius=r))
        elif filter_type == "sharpen":
            filtered_image = result_image.filter(ImageFilter.SHARPEN)
            if intensity != 1.0:
                filtered_image = Image.blend(result_image, filtered_image, min(intensity, 1.0))
        elif filter_type == "emboss":
            filtered_image = result_image.filter(ImageFilter.EMBOSS)
            if intensity != 1.0:
                filtered_image = Image.blend(result_image, filtered_image, min(intensity, 1.0))
        elif filter_type == "smooth":
            filtered_image = result_image.filter(ImageFilter.SMOOTH_MORE if intensity > 1.5 else ImageFilter.SMOOTH)
        else:
            filtered_image = result_image
        result_image = filtered_image
    return result_image
