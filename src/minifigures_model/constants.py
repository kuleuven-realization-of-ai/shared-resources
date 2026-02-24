"""Model constants."""

from pathlib import Path


def get_data_root() -> Path:
    """Return the data folder."""
    return Path(__file__).parents[2] / "data"


def get_data_folder() -> Path:
    """Return the data folder."""
    return get_data_root() / "data"


def get_models_folder() -> Path:
    """Return the models folder."""
    return get_data_root() / "models"
