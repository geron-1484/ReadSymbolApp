from typing import Tuple
from PIL import Image
import io

def encode_jpeg_from_pil(image: Image.Image, quality: int = 85) -> bytes:
    b = io.BytesIO()
    image.save(b, format="JPEG", quality=quality)
    return b.getvalue()

def decode_jpeg_to_pil(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data))

def resize_keep_aspect(img: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    img.thumbnail(max_size)
    return img
