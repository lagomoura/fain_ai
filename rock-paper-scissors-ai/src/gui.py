"""High-level frame composition utilities for the modern GUI.

Phase 1 implements a very simple layout:
    ┌─────────────────────────────┐
    │  720×720 webcam feed        │
    ├─────────────────────────────┤   1280×720 canvas
    │             HUD (right)    │
    └─────────────────────────────┘

Later phases will replace the HUD with prettier components and animations.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

import cv2
import numpy as np


_CANVAS_W = 1280
_CANVAS_H = 720
_WEBCAM_S = 720  # square side for webcam region


class UIState:
    """Lightweight container holding visual state for compose_frame."""

    __slots__ = (
        "player_choice",
        "computer_choice",
        "scores",
        "difficulty",
        "images",
    )

    def __init__(
        self,
        player_choice: str,
        computer_choice: str,
        scores: Dict[str, int],
        difficulty: str,
        images: Dict[str, np.ndarray],
    ) -> None:
        self.player_choice = player_choice
        self.computer_choice = computer_choice
        self.scores = scores
        self.difficulty = difficulty
        self.images = images


# ----------------------------------------------------------------------------
# Background helpers
# ----------------------------------------------------------------------------


def _load_background() -> np.ndarray:
    """Load UI background or create a fallback gradient."""
    assets_dir = Path(__file__).resolve().parent.parent / "assets" / "ui"
    for fname in ("background.png", "background.jpg"):
        bg_path = assets_dir / fname
        if bg_path.exists():
            bg = cv2.imread(str(bg_path))
            if bg is not None:
                return cv2.resize(bg, (_CANVAS_W, _CANVAS_H))
    # Fallback – dark grey gradient
    gradient = np.zeros((_CANVAS_H, _CANVAS_W, 3), dtype=np.uint8)
    for y in range(_CANVAS_H):
        shade = int(30 + 40 * (y / _CANVAS_H))
        gradient[y, :, :] = (shade, shade, shade)
    return gradient


_BACKGROUND: np.ndarray = _load_background()


# ----------------------------------------------------------------------------
# Composition
# ----------------------------------------------------------------------------


def compose_frame(webcam_frame: np.ndarray, state: UIState) -> np.ndarray:
    """Return a 1280×720 frame composed of webcam + HUD."""
    # Ensure webcam frame is square and the expected size
    h, w = webcam_frame.shape[:2]
    # Crop to square centred region
    if w != h:
        side = min(h, w)
        y0 = (h - side) // 2
        x0 = (w - side) // 2
        webcam_frame = webcam_frame[y0 : y0 + side, x0 : x0 + side]
    webcam_frame = cv2.resize(webcam_frame, (_WEBCAM_S, _WEBCAM_S))

    # Copy background to avoid mutating global
    canvas = _BACKGROUND.copy()
    # Place webcam at (0,0)
    canvas[0:_WEBCAM_S, 0:_WEBCAM_S] = webcam_frame

    # Draw HUD on the right panel
    _draw_hud(canvas, state)

    return canvas


# ----------------------------------------------------------------------------
# HUD drawing helpers (very simple for Phase 1)
# ----------------------------------------------------------------------------


def _draw_hud(frame: np.ndarray, state: UIState) -> None:
    """Draw scores, difficulty, and icons on *frame* (in-place)."""
    # Region start x coordinate for HUD
    x0 = _WEBCAM_S + 20

    # Icons (100×100) positions
    if state.player_choice in state.images:
        icon = state.images[state.player_choice]
        frame[50 : 150, x0 : x0 + 100] = icon[:, :, :3]
    if state.computer_choice in state.images:
        icon = state.images[state.computer_choice]
        frame[200 : 300, x0 : x0 + 100] = icon[:, :, :3]

    # Scores
    cv2.putText(
        frame,
        f"You: {state.scores['player']}",
        (x0, 350),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"AI: {state.scores['computer']}",
        (x0, 400),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    # Difficulty
    cv2.putText(
        frame,
        f"Difficulty: {state.difficulty.title()}",
        (x0, 470),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )
