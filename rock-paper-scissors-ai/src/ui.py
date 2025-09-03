from __future__ import annotations

"""UI facade for main loop.

Provides *display_ui* expected by ``main.py``. It converts the raw parameters
into a ``UIState`` and composes a full 1280×720 frame using ``compose_frame``
from ``src.gui``. The function mutates the input *frame* in-place so the caller
can continue to use the same reference.
"""

from typing import Dict

import cv2
import numpy as np

from .gui import UIState, compose_frame

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def display_ui(
    frame: np.ndarray,
    player_choice: str,
    computer_choice: str,
    _winner: str,  # Unused for now; kept for signature compatibility
    scores: Dict[str, int],
    images: Dict[str, np.ndarray],
    *,
    difficulty: str = "normal",
) -> None:
    """Augment *frame* with HUD elements.

    This is a thin wrapper translating the arguments used in ``main.py`` to the
    ``compose_frame`` helper.

    Parameters
    ----------
    frame : np.ndarray
        The current webcam (BGR) frame. Modified in-place.
    player_choice, computer_choice : str
        Current gestures.
    _winner : str
        Ignored placeholder to keep the original call site unchanged.
    scores : Dict[str, int]
        Scoreboard with keys ``'player'`` and ``'computer'``.
    images : Dict[str, np.ndarray]
        Pre-loaded gesture icons.
    difficulty : str, optional
        Difficulty label displayed in the HUD.
    """

    state = UIState(
        player_choice=player_choice,
        computer_choice=computer_choice,
        scores=scores,
        difficulty=difficulty,
        images=images,
    )

    composed = compose_frame(frame, state)

    # Copy composed frame back to the provided array to avoid reallocations in
    # the caller. Ensure shapes match (they should given compose_frame's spec).
    if frame.shape == composed.shape:
        frame[:, :] = composed
    else:
        # If shapes differ, resize caller's frame and assign.
        resized = cv2.resize(composed, (frame.shape[1], frame.shape[0]))
        frame[:, :] = resized
