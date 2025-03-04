"""Endpoints for data operations."""

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from minifigures_model.constants import get_data_folder

router = APIRouter()


@router.get(
    "/get_image/",
    tags=["data"],
    response_model=BaseModel,
    response_class=FileResponse,
    responses={
        200: {"content": {"image/png": {}}},
        404: {
            "content": {"application/json": {}},
            "description": "Image Not Found",
        },
    },
)
def get_image(tag: str) -> FileResponse:
    """Get an image from the database."""
    path = get_data_folder() / f"minifigures/{tag}.png"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Image Not Found")
    return FileResponse(path)


@router.get(
    "/get_image_tags/",
    tags=["data"],
    response_model=list[str],
    response_class=JSONResponse,
    responses={200: {"model": list[str]}},
)
def get_image_tags() -> list[str]:
    """Get all image tags in index file."""
    files = (get_data_folder() / "minifigures").glob("*.png")
    return sorted([file.stem for file in files])
