import cv2
import time
import random
from pathlib import Path
import numpy as np
import mediapipe as mp
from typing import List, Tuple, Optional

from PIL import Image, ImageDraw, ImageFont

from ar_catcher.camera import Camera
from ar_catcher.detector import HandTracker
from ar_catcher.objects import GameObject, ObjectSpawner
from ar_catcher.sprite_manager import blit_alpha, SpriteManager


class Game:
    # Each player keeps an individual score; index 0 → Player 1, index 1 → Player 2.
    PLAYER_COLORS: List[Tuple[int, int, int]] = [(0, 0, 255), (0, 255, 0)]  # BGR
    GOAL: int = 10

    # Preload modern font (Roboto). Font file should be placed in
    # ar_catcher/assets/Roboto-Bold.ttf. Fallback to default if missing.
    FONT_PATH: Path = (
        Path(__file__).resolve().parent / "assets" / "Roboto-Bold.ttf"
    )
    _font_cache: dict[int, ImageFont.FreeTypeFont] = {}

    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.tracker = HandTracker()
        self.spawner = ObjectSpawner(width, height)
        self.objects: List[GameObject] = []
        # Two-player scoreboard
        self.scores: List[int] = [0, 0]
        self.winner: Optional[int] = None  # 0 or 1 when someone reaches the goal
        # Transient visual elements ------------------------------------------------
        self.popups: List[dict] = []  # each: {x, y, text, color, life, ttl}
        self.particles: List[dict] = []  # ambient background particles
        self._init_particles(count=60)
        self.last_spawn = 0.0
        self.spawn_interval = 1.0  # seconds

    def run(self):
        with Camera() as cam:
            # Prepare full-screen window before any frame is shown
            cv2.namedWindow("AR Catcher", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(
                "AR Catcher", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
            )

            prev_time = time.time()

            # Countdown before match starts -------------------------------------
            self._countdown(cam)

            while True:
                frame = cam.read()
                frame = cv2.resize(frame, (self.width, self.height))
                # Mirror correction: flip horizontally so movement matches screen direction
                frame = cv2.flip(frame, 1)

                curr_time = time.time()
                dt = curr_time - prev_time
                prev_time = curr_time

                # Spawn objects
                if curr_time - self.last_spawn > self.spawn_interval:
                    self.objects.append(self.spawner.spawn())
                    self.last_spawn = curr_time

                # Update objects
                for obj in self.objects:
                    obj.update(dt)

                # Remove off-screen objects
                self.objects = [o for o in self.objects if not o.is_off_screen(self.height)]

                # Hand detection -------------------------------------------------
                results = self.tracker.process(frame)
                # (x, y, player_id)
                hand_pixels: List[Tuple[int, int, int]] = []

                if results.multi_hand_landmarks:
                    for pid, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        if pid > 1:  # support max two players
                            break
                        pixels = HandTracker.landmarks_to_pixels(
                            hand_landmarks, self.width, self.height
                        )
                        tip_x, tip_y = pixels[HandTracker.INDEX_TIP_ID]
                        hand_pixels.append((tip_x, tip_y, pid))

                        # Custom colored skeleton per player
                        mp.solutions.drawing_utils.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.tracker._mp_hands.HAND_CONNECTIONS,
                            mp.solutions.drawing_utils.DrawingSpec(color=self.PLAYER_COLORS[pid], thickness=2, circle_radius=2),
                            mp.solutions.drawing_utils.DrawingSpec(color=self.PLAYER_COLORS[pid], thickness=2),
                        )

                # Collision detection --------------------------------------------
                for hx, hy, pid in hand_pixels:
                    for obj in self.objects:
                        dx, dy = hx - obj.x, hy - obj.y
                        if (dx * dx + dy * dy) <= obj.radius * obj.radius:
                            if obj.sprite_name == "bomb":
                                self.scores[pid] -= 2
                                popup_text, popup_color = "-2", (0, 0, 255)
                                # Quick red flash to indicate explosion
                                self._flash_screen(frame, (0, 0, 255))
                            else:
                                self.scores[pid] += 1
                                popup_text, popup_color = "+1", self.PLAYER_COLORS[pid]

                            self.objects.remove(obj)

                            self._add_popup(x=hx, y=hy, text=popup_text, color=popup_color)

                            # Check for winner
                            if self.scores[pid] >= self.GOAL:
                                self.winner = pid
                            break

                # Draw objects
                for obj in self.objects:
                    sprite_bgr, alpha = SpriteManager.get(obj.sprite_name, obj.radius * 2)
                    blit_alpha(frame, sprite_bgr, alpha, (int(obj.x), int(obj.y)))

                # ---------------- Ambient background particles -------------------
                self._update_and_draw_particles(frame, dt)

                # ------------------- UI: two-player score boxes ------------------
                self._draw_glass_panel(frame, (10, 10), (220, 60))
                self._draw_glass_panel(
                    frame,
                    (self.width - 230, 10),
                    (220, 60),
                )

                # Outlined score texts using modern font
                p1_text = f"P1: {self.scores[0]}"
                p2_text = f"P2: {self.scores[1]}"

                self._draw_text_modern(frame, p1_text, (20, 20), 36, self.PLAYER_COLORS[0])
                self._draw_text_modern(frame, p2_text, (self.width - 200, 20), 36, self.PLAYER_COLORS[1])

                # Floating pop-ups -----------------------------------------------
                self._update_and_draw_popups(frame, dt)

                # Victory condition overlay --------------------------------------
                if self.winner is not None:
                    win_overlay = frame.copy()
                    msg = f"PLAYER {self.winner + 1} WINS!"
                    cv2.rectangle(
                        win_overlay,
                        (0, self.height // 2 - 60),
                        (self.width, self.height // 2 + 60),
                        (0, 0, 0),
                        -1,
                    )
                    cv2.addWeighted(win_overlay, 0.7, frame, 0.3, 0, frame)
                    self._draw_text_modern(
                        frame,
                        msg,
                        (self.width // 2 - 300, self.height // 2 - 20),
                        72,
                        self.PLAYER_COLORS[self.winner],
                        center=False,
                    )

                    cv2.imshow("AR Catcher", frame)
                    cv2.waitKey(3000)  # show for 3 seconds
                    break

                cv2.imshow("AR Catcher", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        cv2.destroyAllWindows()

    # ---------------------------------------------------------------------
    # Helper methods for visual effects
    # ---------------------------------------------------------------------

    def _init_particles(self, count: int = 40) -> None:
        """Initialize a background particle field."""
        for _ in range(count):
            self.particles.append(
                {
                    "x": random.uniform(0, self.width),
                    "y": random.uniform(0, self.height),
                    "radius": random.randint(1, 3),
                    "speed": random.uniform(20, 40),
                    "alpha": random.uniform(0.05, 0.15),
                    "color": (255, 255, 255),
                }
            )

    def _update_and_draw_particles(self, frame, dt: float) -> None:
        """Move particles downward; wrap to top when leaving screen."""
        overlay = frame.copy()
        for p in self.particles:
            p["y"] += p["speed"] * dt
            if p["y"] - p["radius"] > self.height:
                p["y"] = -p["radius"]
                p["x"] = random.uniform(0, self.width)

            cv2.circle(
                overlay,
                (int(p["x"]), int(p["y"])),
                p["radius"],
                p["color"],
                -1,
            )

        cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)

    # --------------------------- Floating popups -------------------------
    def _add_popup(self, x: int, y: int, text: str, color: Tuple[int, int, int]) -> None:
        self.popups.append(
            {
                "x": x,
                "y": y,
                "text": text,
                "color": color,
                "life": 0.0,
                "ttl": 1.0,  # seconds
            }
        )

    def _update_and_draw_popups(self, frame, dt: float) -> None:
        remain: List[dict] = []
        for pop in self.popups:
            pop["life"] += dt
            if pop["life"] > pop["ttl"]:
                continue

            # Rising effect
            progress = pop["life"] / pop["ttl"]
            y_off = int(progress * -40)
            alpha = 1.0 - progress  # fade out

            overlay = frame.copy()
            self._draw_text_modern(
                overlay,
                pop["text"],
                (int(pop["x"]), int(pop["y"] + y_off)),
                30,
                pop["color"],
            )
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            remain.append(pop)

        self.popups = remain

    # --------------------------- Screen flash ----------------------------
    def _flash_screen(self, frame, color: Tuple[int, int, int]) -> None:
        overlay = frame.copy()
        overlay[:] = color
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

    # ---------------------- Modern text rendering ------------------------
    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        if size in self._font_cache:
            return self._font_cache[size]
        if self.FONT_PATH.exists():
            font = ImageFont.truetype(str(self.FONT_PATH), size)
        else:
            font = ImageFont.load_default()
        self._font_cache[size] = font
        return font

    def _draw_text_modern(
        self,
        frame,
        text: str,
        pos: Tuple[int, int],
        size: int,
        color: Tuple[int, int, int] = (255, 255, 255),
        center: bool = False,
    ) -> None:
        """Draw anti-aliased text using Pillow for modern look."""
        b, g, r = color  # convert to RGB
        rgb_color = (r, g, b)

        # Create transparent canvas
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        font = self._get_font(size)

        x, y = pos
        if center:
            # Pillow >= 8 provides textbbox; fall back to textsize otherwise
            if hasattr(draw, "textbbox"):
                bbox = draw.textbbox((0, 0), text, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x -= w // 2
                y -= h // 2
            else:
                w, h = draw.textsize(text, font=font)  # type: ignore[arg-type]

        draw.text((x, y), text, font=font, fill=rgb_color)

        frame[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # -------------------------- Glass panels -----------------------------
    def _draw_glass_panel(self, frame, top_left: Tuple[int, int], size: Tuple[int, int]) -> None:
        x, y = top_left
        w, h = size

        # Extract region, blur it, and merge back for frosted effect
        roi = frame[y : y + h, x : x + w]
        blurred = cv2.GaussianBlur(roi, (15, 15), 0)
        frame[y : y + h, x : x + w] = blurred

        # Neon outline
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

    # -------------------------- Countdown -------------------------------
    def _countdown(self, cam) -> None:
        """Display 3-2-1-GO before the main loop."""
        for text in ["3", "2", "1", "GO"]:
            frame = cam.read()
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.flip(frame, 1)

            overlay = frame.copy()
            self._draw_text_modern(
                overlay,
                text,
                (self.width // 2, self.height // 2),
                120,
                (255, 255, 255),
                center=True,
            )
            cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

            cv2.imshow("AR Catcher", frame)
            cv2.waitKey(800)


# -------------------------------------------------------------------------
# Script entry point
# -------------------------------------------------------------------------


if __name__ == "__main__":
    Game().run()
