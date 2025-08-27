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
from ar_catcher.objects import GameObject, ObjectSpawner, ObjectType
from ar_catcher.sprite_manager import blit_alpha, SpriteManager


class Game:
    # Each player keeps an individual score; index 0 → Player 1, index 1 → Player 2.
    PLAYER_COLORS: List[Tuple[int, int, int]] = [(0, 0, 255), (0, 255, 0)]  # BGR
    GOAL: int = 15  # Increased goal for longer gameplay
    
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
        
        # Power-up system
        self.player_shields: List[bool] = [False, False]  # Shield protection
        self.shield_timers: List[float] = [0.0, 0.0]  # Shield duration
        self.combo_multipliers: List[int] = [1, 1]  # Score multipliers
        self.combo_timers: List[float] = [0.0, 0.0]  # Combo duration
        
        # Game state
        self.game_time = 0.0  # Track total game time
        
        # Transient visual elements ------------------------------------------------
        self.popups: List[dict] = []  # each: {x, y, text, color, life, ttl, scale}
        self.particles: List[dict] = []  # ambient background particles
        self.explosions: List[dict] = []  # explosion effects
        self._init_particles(count=80)  # More particles for better atmosphere
        self.last_spawn = 0.0
        self.spawn_interval = 0.8  # Faster spawning for more action

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
                
                self.game_time += dt

                # Update difficulty and spawn objects
                self.spawner.update_difficulty(dt)
                if curr_time - self.last_spawn > self.spawn_interval:
                    self.objects.append(self.spawner.spawn())
                    self.last_spawn = curr_time

                # Update objects
                for obj in self.objects:
                    obj.update(dt)

                # Remove off-screen objects
                self.objects = [o for o in self.objects if not o.is_off_screen(self.height)]

                # Update power-ups
                self._update_power_ups(dt)

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
                            self._handle_collision(obj, pid, hx, hy)
                            break

                # Draw objects with enhanced effects
                for obj in self.objects:
                    self._draw_object_with_effects(frame, obj)

                # ---------------- Ambient background particles -------------------
                self._update_and_draw_particles(frame, dt)

                # ------------------- UI: Enhanced two-player score boxes --------
                self._draw_enhanced_ui(frame)

                # Floating pop-ups -----------------------------------------------
                self._update_and_draw_popups(frame, dt)
                
                # Explosion effects
                self._update_and_draw_explosions(frame, dt)

                # Victory condition overlay --------------------------------------
                if self.winner is not None:
                    self._show_victory_screen(frame)
                    break

                cv2.imshow("AR Catcher", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("p"):
                    # Pause functionality
                    self._pause_game(frame)

        cv2.destroyAllWindows()

    def _handle_collision(self, obj: GameObject, player_id: int, x: int, y: int):
        """Handle collision between player and game object."""
        # Remove the object
        self.objects.remove(obj)
        
        # Handle different object types
        if obj.object_type in [ObjectType.BOMB, ObjectType.MEGA_BOMB, ObjectType.CLUSTER_BOMB]:
            if self.player_shields[player_id]:
                # Shield protects from bombs
                self._add_popup(x, y, "SHIELDED!", (255, 255, 0), scale=1.5)
                self.player_shields[player_id] = False
                self.shield_timers[player_id] = 0.0
                
                # Create shield break effect
                self._create_shield_break_effect(x, y)
            else:
                # Apply bomb effects
                score_change = obj.score_value
                self.scores[player_id] += score_change
                
                # Reset combo on bomb hit
                self.combo_multipliers[player_id] = 1
                self.combo_timers[player_id] = 0.0
                
                # Create explosion effect
                self._create_explosion(x, y, obj.object_type)
                
                # Different flash colors for different bomb types
                if obj.object_type == ObjectType.MEGA_BOMB:
                    popup_text = f"{score_change}"
                    popup_color = (0, 0, 255)
                elif obj.object_type == ObjectType.CLUSTER_BOMB:
                    popup_text = f"{score_change}"
                    popup_color = (0, 255, 255)
                else:
                    popup_text = f"{score_change}"
                    popup_color = (0, 0, 255)
                
                self._add_popup(x, y, popup_text, popup_color, scale=1.2)
                
        elif obj.object_type == ObjectType.SHIELD:
            # Activate shield power-up
            self.player_shields[player_id] = True
            self.shield_timers[player_id] = 8.0  # 8 seconds duration
            self._add_popup(x, y, "SHIELD!", (255, 255, 0), scale=1.5)
            
            # Create power-up aura effect
            self._create_power_up_effect(x, y, (255, 255, 0))
            
        elif obj.object_type == ObjectType.GOLDEN_FRUIT:
            # Golden fruit gives bonus points and extends combo
            bonus_score = obj.score_value * self.combo_multipliers[player_id]
            self.scores[player_id] += bonus_score
            self.combo_multipliers[player_id] = min(5, self.combo_multipliers[player_id] + 1)
            self.combo_timers[player_id] = 5.0  # 5 seconds to maintain combo
            
            self._add_popup(x, y, f"+{bonus_score}", (255, 215, 0), scale=1.8)
            
            # Create golden sparkle effect
            self._create_sparkle_effect(x, y, (255, 215, 0))
            
        else:
            # Regular fruits
            base_score = obj.score_value
            combo_score = base_score * self.combo_multipliers[player_id]
            self.scores[player_id] += combo_score
            
            # Extend combo
            self.combo_multipliers[player_id] = min(5, self.combo_multipliers[player_id] + 1)
            self.combo_timers[player_id] = 5.0
            
            popup_text = f"+{combo_score}"
            popup_color = self.PLAYER_COLORS[player_id]
            if self.combo_multipliers[player_id] > 1:
                popup_text += f" x{self.combo_multipliers[player_id]}"
                popup_color = (255, 215, 0)  # Gold for combo
            
            self._add_popup(x, y, popup_text, popup_color, scale=1.0)

        # Check for winner
        if self.scores[player_id] >= self.GOAL:
            self.winner = player_id

    def _update_power_ups(self, dt: float):
        """Update power-up timers and effects."""
        for i in range(2):
            # Update shield timers
            if self.player_shields[i]:
                self.shield_timers[i] -= dt
                if self.shield_timers[i] <= 0:
                    self.player_shields[i] = False
            
            # Update combo timers
            if self.combo_timers[i] > 0:
                self.combo_timers[i] -= dt
                if self.combo_timers[i] <= 0:
                    self.combo_multipliers[i] = 1

    def _draw_object_with_effects(self, frame, obj: GameObject):
        """Draw objects with enhanced visual effects."""
        sprite_bgr, alpha = SpriteManager.get(obj.sprite_name, obj.radius * 2)
        
        # Add glow effects for special objects
        if obj.object_type == ObjectType.GOLDEN_FRUIT:
            # Golden glow effect
            glow_radius = int(obj.radius * 1.5)
            cv2.circle(frame, (int(obj.x), int(obj.y)), glow_radius, (0, 215, 255), 3)
        elif obj.object_type == ObjectType.SHIELD:
            # Shield glow effect
            glow_radius = int(obj.radius * 1.3)
            cv2.circle(frame, (int(obj.x), int(obj.y)), glow_radius, (0, 255, 255), 2)
        elif obj.object_type in [ObjectType.MEGA_BOMB, ObjectType.CLUSTER_BOMB]:
            # Danger glow effect
            glow_radius = int(obj.radius * 1.4)
            color = (0, 0, 255) if obj.object_type == ObjectType.MEGA_BOMB else (0, 255, 255)
            cv2.circle(frame, (int(obj.x), int(obj.y)), glow_radius, color, 2)
        
        blit_alpha(frame, sprite_bgr, alpha, (int(obj.x), int(obj.y)))

    def _create_explosion(self, x: int, y: int, bomb_type: ObjectType):
        """Create explosion particle effect."""
        particle_count = 15 if bomb_type == ObjectType.MEGA_BOMB else 10
        for _ in range(particle_count):
            self.explosions.append({
                "x": x + random.uniform(-20, 20),
                "y": y + random.uniform(-20, 20),
                "vx": random.uniform(-100, 100),
                "vy": random.uniform(-150, -50),
                "life": 0.0,
                "ttl": random.uniform(0.5, 1.0),
                "size": random.randint(2, 6),
                "color": (0, 0, 255) if bomb_type == ObjectType.MEGA_BOMB else (0, 255, 255)
            })

    def _create_shield_break_effect(self, x: int, y: int):
        """Create shield break visual effect."""
        for _ in range(8):
            self.explosions.append({
                "x": x + random.uniform(-15, 15),
                "y": y + random.uniform(-15, 15),
                "vx": random.uniform(-80, 80),
                "vy": random.uniform(-100, -30),
                "life": 0.0,
                "ttl": random.uniform(0.8, 1.2),
                "size": random.randint(3, 8),
                "color": (255, 255, 0)  # Yellow for shield
            })

    def _create_power_up_effect(self, x: int, y: int, color: Tuple[int, int, int]):
        """Create power-up activation effect."""
        for _ in range(12):
            self.explosions.append({
                "x": x + random.uniform(-25, 25),
                "y": y + random.uniform(-25, 25),
                "vx": random.uniform(-60, 60),
                "vy": random.uniform(-80, -20),
                "life": 0.0,
                "ttl": random.uniform(1.0, 1.5),
                "size": random.randint(2, 5),
                "color": color
            })

    def _create_sparkle_effect(self, x: int, y: int, color: Tuple[int, int, int]):
        """Create sparkle effect for golden items."""
        for _ in range(6):
            self.explosions.append({
                "x": x + random.uniform(-20, 20),
                "y": y + random.uniform(-20, 20),
                "vx": random.uniform(-40, 40),
                "vy": random.uniform(-60, -10),
                "life": 0.0,
                "ttl": random.uniform(0.6, 1.0),
                "size": random.randint(1, 4),
                "color": color
            })

    def _update_and_draw_explosions(self, frame, dt: float):
        """Update and draw explosion effects."""
        remain = []
        for exp in self.explosions:
            exp["life"] += dt
            if exp["life"] > exp["ttl"]:
                continue
                
            # Update position
            exp["x"] += exp["vx"] * dt
            exp["y"] += exp["vy"] * dt
            
            # Draw particle
            alpha = 1.0 - (exp["life"] / exp["ttl"])
            size = int(exp["size"] * alpha)
            if size > 0:
                cv2.circle(frame, (int(exp["x"]), int(exp["y"])), size, exp["color"], -1)
            
            remain.append(exp)
        self.explosions = remain

    def _draw_enhanced_ui(self, frame):
        """Draw enhanced UI with power-up indicators."""
        # Player 1 UI (left)
        self._draw_glass_panel(frame, (10, 10), (280, 100))
        p1_text = f"P1: {self.scores[0]}"
        self._draw_text_modern(frame, p1_text, (20, 20), 36, self.PLAYER_COLORS[0])
        
        # Power-up indicators for P1
        if self.player_shields[0]:
            self._draw_text_modern(frame, "🛡️", (20, 60), 24, (255, 255, 0))
        if self.combo_multipliers[0] > 1:
            self._draw_text_modern(frame, f"x{self.combo_multipliers[0]}", (50, 60), 24, (255, 215, 0))
        
        # Player 2 UI (right)
        self._draw_glass_panel(frame, (self.width - 290, 10), (280, 100))
        p2_text = f"P2: {self.scores[1]}"
        self._draw_text_modern(frame, p2_text, (self.width - 280, 20), 36, self.PLAYER_COLORS[1])
        
        # Power-up indicators for P2
        if self.player_shields[1]:
            self._draw_text_modern(frame, "🛡️", (self.width - 280, 60), 24, (255, 255, 0))
        if self.combo_multipliers[1] > 1:
            self._draw_text_modern(frame, f"x{self.combo_multipliers[1]}", (self.width - 250, 60), 24, (255, 215, 0))
        
        # Game time and difficulty indicator
        self._draw_glass_panel(frame, (self.width // 2 - 100, 10), (200, 50))
        time_text = f"Time: {int(self.game_time)}s"
        self._draw_text_modern(frame, time_text, (self.width // 2 - 90, 20), 24, (255, 255, 255), center=False)
        
        # Bomb spawn rate indicator
        bomb_text = f"Bombs: {int(self.spawner.bomb_spawn_rate * 100)}%"
        self._draw_text_modern(frame, bomb_text, (self.width // 2 - 90, 45), 18, (255, 100, 100), center=False)

    def _pause_game(self, frame):
        """Pause the game and show pause screen."""
        pause_overlay = frame.copy()
        cv2.rectangle(
            pause_overlay,
            (0, 0),
            (self.width, self.height),
            (0, 0, 0),
            -1,
        )
        cv2.addWeighted(pause_overlay, 0.8, frame, 0.2, 0, frame)
        
        self._draw_text_modern(
            frame,
            "PAUSED",
            (self.width // 2, self.height // 2 - 50),
            72,
            (255, 255, 255),
            center=True,
        )
        self._draw_text_modern(
            frame,
            "Press P to resume",
            (self.width // 2, self.height // 2 + 50),
            36,
            (200, 200, 200),
            center=True,
        )
        
        cv2.imshow("AR Catcher", frame)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("p"):
                break
            elif key == ord("q"):
                self.winner = -1  # Force exit
                break

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
    def _add_popup(self, x: int, y: int, text: str, color: Tuple[int, int, int], scale: float = 1.0) -> None:
        self.popups.append(
            {
                "x": x,
                "y": y,
                "text": text,
                "color": color,
                "life": 0.0,
                "ttl": 1.0,  # seconds
                "scale": scale,
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
            # Apply scale to font size
            font_size = int(30 * pop.get("scale", 1.0))
            self._draw_text_modern(
                overlay,
                pop["text"],
                (int(pop["x"]), int(pop["y"] + y_off)),
                font_size,
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

    def _show_victory_screen(self, frame):
        """Show the victory screen and wait for key press."""
        victory_overlay = frame.copy()
        cv2.rectangle(
            victory_overlay,
            (0, self.height // 2 - 60),
            (self.width, self.height // 2 + 60),
            (0, 0, 0),
            -1,
        )
        cv2.addWeighted(victory_overlay, 0.7, frame, 0.3, 0, frame)
        
        msg = f"PLAYER {self.winner + 1} WINS!"
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


# -------------------------------------------------------------------------
# Script entry point
# -------------------------------------------------------------------------


if __name__ == "__main__":
    Game().run()
