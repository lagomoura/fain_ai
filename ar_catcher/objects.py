import random
from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum

from .sprite_manager import SpriteManager


class ObjectType(Enum):
    """Game object types with their properties."""
    APPLE = ("apple", 26, 1, "🍎")
    ORANGE = ("orange", 32, 1, "🍊")
    POKEBALL = ("pokeball", 26, 2, "⚡")
    BOMB = ("bomb", 28, -2, "💣")
    MEGA_BOMB = ("bomb2", 35, -3, "💥")  # Bigger, more dangerous
    CLUSTER_BOMB = ("cluster", 22, -1, "💥")  # Smaller, faster
    GOLDEN_FRUIT = ("goldFruit", 30, 3, "🌟")  # Rare bonus item
    SHIELD = ("shield", 25, 0, "🛡️")  # Temporary protection


@dataclass
class GameObject:
    x: float
    y: float
    radius: int
    velocity_y: float
    sprite_name: str
    object_type: ObjectType
    score_value: int
    special_effect: Optional[str] = None

    @property
    def sprite(self) -> Tuple:
        return SpriteManager.get(self.sprite_name)

    def update(self, dt: float):
        self.y += self.velocity_y * dt

        # Add some horizontal movement for more dynamic gameplay
        if self.object_type in [ObjectType.CLUSTER_BOMB, ObjectType.MEGA_BOMB]:
            self.x += random.uniform(-20, 20) * dt

    def is_off_screen(self, screen_height: int) -> bool:
        return self.y - self.radius > screen_height


class ObjectSpawner:
    def __init__(self, screen_width: int, screen_height: int):
        self.sw = screen_width
        self.sh = screen_height
        self.difficulty_timer = 0.0
        self.bomb_spawn_rate = 0.4  # Start with 40% bomb chance

    def update_difficulty(self, dt: float):
        """Increase difficulty over time."""
        self.difficulty_timer += dt
        # Increase bomb spawn rate every 30 seconds
        if self.difficulty_timer > 30.0:
            self.bomb_spawn_rate = min(0.7, self.bomb_spawn_rate + 0.05)
            self.difficulty_timer = 0.0

    def spawn(self):
        x = random.randint(20, self.sw - 20)
        y = -20

        # Determine object type based on probabilities
        rand_val = random.random()

        if rand_val < self.bomb_spawn_rate:
            # Bomb types with different probabilities
            bomb_rand = random.random()
            if bomb_rand < 0.5:
                obj_type = ObjectType.BOMB
            elif bomb_rand < 0.8:
                obj_type = ObjectType.CLUSTER_BOMB
            else:
                obj_type = ObjectType.MEGA_BOMB
        elif rand_val < self.bomb_spawn_rate + 0.05:  # 5% chance for golden fruit
            obj_type = ObjectType.GOLDEN_FRUIT
        elif rand_val < self.bomb_spawn_rate + 0.08:  # 3% chance for shield
            obj_type = ObjectType.SHIELD
        else:
            # Regular fruits
            obj_type = random.choice([ObjectType.APPLE, ObjectType.ORANGE, ObjectType.POKEBALL])

        # Set properties based on object type
        if obj_type == ObjectType.MEGA_BOMB:
            radius = 35
            velocity = random.uniform(80, 150)  # Slower but bigger
        elif obj_type == ObjectType.CLUSTER_BOMB:
            radius = 22
            velocity = random.uniform(200, 280)  # Faster but smaller
        elif obj_type == ObjectType.GOLDEN_FRUIT:
            radius = 30
            velocity = random.uniform(100, 180)
        elif obj_type == ObjectType.SHIELD:
            radius = 25
            velocity = random.uniform(150, 220)
        else:
            radius = obj_type.value[1]
            velocity = random.uniform(120, 220)

        return GameObject(
            x=x,
            y=y,
            radius=radius,
            velocity_y=velocity,
            sprite_name=obj_type.value[0],
            object_type=obj_type,
            score_value=obj_type.value[2]
        )
