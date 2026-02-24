"""Endpoint for model predictions."""

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from minifigures_api.routers.basemodels import Prediction
from minifigures_api.routers.utils import extract_images_from_files, fetch_model

router = APIRouter()


@router.post(
    "/image/",
    tags=["prediction"],
    response_model=Prediction,
    response_class=JSONResponse,
    responses={
        200: {"model": Prediction},
        404: {
            "content": {"application/json": {}},
            "description": "Model Not Found",
        },
        415: {
            "content": {"application/json": {}},
            "description": "Media type not valid",
        },
    },
)
def predict(file: UploadFile) -> Prediction:
    """Use the tagged model to predict over an image."""
    # Convert the UploadFile to a torch Tensor
    file = extract_images_from_files([file])[0]

    # Make a prediction
    model = fetch_model()
    prediction = model.predict(file)

    # Return the result
    return Prediction(prediction=prediction)
