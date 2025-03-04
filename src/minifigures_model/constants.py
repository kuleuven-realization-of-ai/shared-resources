"""Utilisation functions."""

from functools import lru_cache
from pathlib import Path


DEFAULT_MODEL_TAG = "20230208T134711-efficientnetb0-final-model"


@lru_cache
def get_root_folder() -> Path:
    """Load in the root folder."""
    folder = Path(__file__).parents[-2] / "data"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


@lru_cache
def get_data_folder() -> Path:
    """Load in the data folder."""
    folder = get_root_folder() / "data"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


@lru_cache
def get_models_folder() -> Path:
    """Load in the model folder."""
    folder = get_root_folder() / "models"
    folder.mkdir(exist_ok=True, parents=True)
    return folder
