"""Minifigures model."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image
from torch import nn
from torchvision import models

from minifigures_model.constants import get_models_folder
from minifigures_model.utils import pil_to_torch, resize


class EncoderDecoder(nn.Module):
    """Create a single EncoderDecoder model."""

    def __init__(
        self,
        tag: str,
        classes: list[str],
        resolution: int = 256,
    ):
        """Initialise the model."""
        super().__init__()

        # Initialise class attributes
        self.tag = tag
        self.classes = sorted(classes)
        self.resolution = resolution

        # Create the encoder
        self.encoder = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        n_features = self.encoder.classifier[1].in_features
        self.encoder.classifier[-1] = torch.nn.Identity()

        # Create the decoder
        self.decoder = nn.Sequential(
            nn.Linear(n_features, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, len(self.classes)),
        )

        # Freeze the encoder
        for param in self.encoder.parameters():
            param.requires_grad = False

    def __str__(self) -> str:
        """String representation of the model."""
        return f"EncoderDecoder({self.tag})"

    def __repr__(self):
        """String representation of the model."""
        return self.__str__()

    def predict(self, x: Image) -> dict[str, float]:
        """Make a prediction for the provided Image."""
        # Reshape into required format
        x_t = pil_to_torch(x)
        x_t = resize(x_t, resolution=self.resolution)

        # Add batch dimension and feed to the model, convert to probabilities
        logits = self.forward(x_t[None,])[0]
        probs = torch.sigmoid(logits).detach().numpy()

        # Transform into probabilistic predictions
        return {k: float(v) for k, v in zip(self.classes, probs)}

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def get_metadata(self) -> dict[str, Any]:
        """Return the model's metadata."""
        return {
            "tag": self.tag,
            "classes": self.classes,
            "resolution": self.resolution,
        }

    def save(self):
        """Save the model."""
        mdl_f = get_models_folder() / self.tag
        mdl_f.mkdir(parents=True, exist_ok=True)

        # Model parameters
        with open(mdl_f / "metadata.json", "w") as f:
            json.dump(
                self.get_metadata(),
                f,
                indent=2,
                sort_keys=True,
            )

        # Model binaries
        torch.save(self.state_dict(), mdl_f / "weights.pt")

    @classmethod
    def load(cls, tag: str):
        """Load the model."""
        # Load metadata first
        with open(get_models_folder() / tag / "metadata.json", "r") as f:
            metadata = json.load(f)

        # Create the model
        model = cls(**metadata)

        # Inject the model's weights
        model.load_state_dict(torch.load(get_models_folder() / tag / "weights.pt"))
        return model
