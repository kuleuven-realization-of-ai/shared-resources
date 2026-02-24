"""Utilisation functions."""

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


def pil_to_torch(x: Image) -> torch.Tensor:
    """Convert a PIL image to a torch Tensor."""
    return torch.Tensor(np.array(x.convert("RGB"))).permute(2, 0, 1) / 255.0


def resize(x: torch.Tensor, resolution: int) -> torch.Tensor:
    """
    Resize a single image (as torch Tensor) to a given resolution.

    Note: The image is first padded into a square, then resized

    Parameters
    ----------
    x : torch.Tensor
        The image to resize
        Shape: (channels, width, height)
    resolution : int
        The resolution to resize to

    Returns
    -------
    torch.Tensor
        The resized image
    """
    # Pad into a square
    _, h, w = x.shape  # channels, width, height
    max_wh = max(w, h)
    p_left, p_right = ((max_wh - w) // 2 for _ in range(2))
    p_right += int(w % 2 == 1)
    p_bottom, p_top = ((max_wh - h) // 2 for _ in range(2))
    p_top += int(h % 2 == 1)
    padding = (p_left, p_right, p_top, p_bottom)
    x = F.pad(x, padding, value=1, mode="constant")

    # Resize
    return F.interpolate(x[None,], size=(resolution, resolution), mode="bilinear")[0]
