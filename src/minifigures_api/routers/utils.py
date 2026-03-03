"""Utilisation functions."""

from functools import lru_cache

from fastapi import UploadFile
from PIL import Image
from starlette.exceptions import HTTPException

from minifigures_model import EncoderDecoder, get_models_folder


def extract_images_from_files(files: list[UploadFile]) -> list[Image.Image]:
    """Extract images from a list of files."""
    extracted = []
    for file in files:
        if file.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(
                status_code=415, detail=f"Media type '{file.content_type}' not valid"
            )
        with Image.open(file.file) as img:
            extracted.append(img.convert("RGB").copy())
    return extracted


@lru_cache
def fetch_model(tag: str = "my_model") -> EncoderDecoder:
    """Fetch a model from the database."""
    if (get_models_folder() / tag).is_dir():
        return EncoderDecoder.load(tag)
    raise HTTPException(status_code=404, detail=f"Model '{tag}' not found")
