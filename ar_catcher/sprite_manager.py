import os
from pathlib import Path
from typing import Dict

import cv2
import numpy as np


ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "sprites"


def load_png(path: Path):
    """Load a PNG with alpha channel."""
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(path)
    # Convert BGRA ➔ BGR + alpha mask
    if img.shape[2] == 4:
        bgr = img[..., :3]
        alpha = img[..., 3] / 255.0
        return bgr, alpha
    else:
        h, w = img.shape[:2]
        alpha = np.ones((h, w), dtype=np.float32)
        return img, alpha


class SpriteManager:
    _cache: Dict[str, tuple] = {}

    @classmethod
    def get(cls, name: str, size: int | None = None):
        """Return (bgr, alpha) of sprite. If size is given, returns a scaled copy (square size x size)."""
        cache_key = f"{name}_{size}" if size else name
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        # Load original if not loaded yet
        if name not in cls._cache:
            file_path = ASSETS_DIR / f"{name}.png"
            cls._cache[name] = load_png(file_path)

        bgr, alpha = cls._cache[name]

        if size is None:
            return bgr, alpha

        # Resize with keeping alpha mask alignment
        bgr_resized = cv2.resize(bgr, (size, size), interpolation=cv2.INTER_AREA)
        alpha_resized = cv2.resize(alpha, (size, size), interpolation=cv2.INTER_AREA)
        cls._cache[cache_key] = (bgr_resized, alpha_resized)
        return cls._cache[cache_key]


def blit_alpha(dst: np.ndarray, sprite_bgr: np.ndarray, alpha: np.ndarray, pos):
    """Draw sprite on dst at pos (center) using alpha blending."""
    x, y = pos
    h, w = sprite_bgr.shape[:2]
    top_left_x = int(x - w / 2)
    top_left_y = int(y - h / 2)

    # Compute clipping
    if top_left_x < 0 or top_left_y < 0 or top_left_x + w > dst.shape[1] or top_left_y + h > dst.shape[0]:
        return  # skip out of bounds for now

    roi = dst[top_left_y : top_left_y + h, top_left_x : top_left_x + w]
    # Blend
    for c in range(3):
        roi[..., c] = roi[..., c] * (1 - alpha) + sprite_bgr[..., c] * alpha
