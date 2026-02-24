"""Utils functions for the Streamlit app."""

import io

import requests
from PIL import Image

from minifigures_app.constants import URL


def predict_image(image: Image.Image) -> dict[str, float]:
    """Get model predictions for a given image using a FastAPI request."""
    # Format the uploaded image
    buff = io.BytesIO()
    image.save(buff, format="PNG")
    img_str = buff.getvalue()

    # Create the prediction
    response = requests.post(
        url=f"{URL}/predict/image/",
        files=[("file", ("UID", img_str, "image/png"))],
    )

    # Return the result
    return response.json()["prediction"]


def list_im_tags() -> list[str]:
    """Get all image tags in index file."""
    response = requests.get(url=f"{URL}/data/get_image_tags/")
    return response.json()


def get_image(tag: str) -> Image.Image:
    """Get an image from the database."""
    response = requests.get(url=f"{URL}/data/get_image/", params={"tag": tag})
    return Image.open(io.BytesIO(response.content))
