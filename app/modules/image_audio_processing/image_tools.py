import base64
from io import BytesIO

from PIL import Image, ImageFilter, ImageOps


def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def load_image_source(image_source):
    if isinstance(image_source, Image.Image):
        return image_source.convert("RGB")
    return Image.open(image_source).convert("RGB")


def image_from_base64(encoded_image):
    return Image.open(BytesIO(base64.b64decode(encoded_image))).convert("RGB")


def apply_image_effect(image_source, effect="grayscale", strength=4):
    strength = max(1, min(int(strength), 12))
    image = load_image_source(image_source)
    image.thumbnail((1100, 760))

    if effect == "grayscale":
        result = ImageOps.grayscale(image).convert("RGB")
    elif effect == "invert":
        result = ImageOps.invert(image)
    elif effect == "blur":
        result = image.filter(ImageFilter.GaussianBlur(radius=strength))
    elif effect == "contour":
        result = image.filter(ImageFilter.CONTOUR)
    elif effect == "mirror":
        result = ImageOps.mirror(image)
    elif effect == "rotate":
        result = image.rotate(90, expand=True)
    elif effect == "pixelate":
        small_width = max(18, image.width // (strength * 2))
        small_height = max(18, image.height // (strength * 2))
        result = image.resize((small_width, small_height), Image.Resampling.BILINEAR)
        result = result.resize(image.size, Image.Resampling.NEAREST)
    elif effect == "sepia":
        gray = ImageOps.grayscale(image)
        result = ImageOps.colorize(gray, "#2b1b12", "#ffd7a1")
    elif effect == "neon":
        edges = image.filter(ImageFilter.FIND_EDGES)
        color = ImageOps.colorize(ImageOps.grayscale(edges), "#08111f", "#00f5d4")
        result = Image.blend(image, color, 0.62)
    else:
        result = image

    return image_to_base64(result)
