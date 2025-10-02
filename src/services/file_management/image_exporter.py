from PIL import Image


def export_image(image: Image.Image, path: str) -> None:
    image.save(path)
