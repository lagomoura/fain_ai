import random
from dataclasses import dataclass
from typing import Tuple

from .sprite_manager import SpriteManager


@dataclass
class GameObject:
    x: float
    y: float
    radius: int
    velocity_y: float
    sprite_name: str

    @property
    def sprite(self) -> Tuple:
        return SpriteManager.get(self.sprite_name)

    def update(self, dt: float):
        self.y += self.velocity_y * dt

    def is_off_screen(self, screen_height: int) -> bool:
        return self.y - self.radius > screen_height


class ObjectSpawner:
    def __init__(self, screen_width: int, screen_height: int):
        self.sw = screen_width
        self.sh = screen_height

    def spawn(self):
        x = random.randint(20, self.sw - 20)
        y = -20
        # 30% chance to spawn a bomb instead of a fruit
        if random.random() < 0.3:
            sprite_choice = "bomb"
            radius = 28
        else:
            sprite_choice = random.choice(["apple", "orange", "pokeball"])
            # Make orange slightly bigger for easier catch
            radius = 32 if sprite_choice == "orange" else 26
        velocity = random.uniform(120, 220)
        return GameObject(x=x, y=y, radius=radius, velocity_y=velocity, sprite_name=sprite_choice)
