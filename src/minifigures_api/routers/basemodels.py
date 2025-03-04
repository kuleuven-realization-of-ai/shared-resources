"""Pydantic basemodels."""

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    """Prediction base model."""

    prediction: dict[str, float] = Field(
        ...,
        title="prediction",
        description="Dictionary containing the predicted probability for each class",
        example={"class1": 0.42, "class2": 0.42},
    )
