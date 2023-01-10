from __future__ import annotations
from pygame.math import Vector2

class VEC(Vector2):
    def normalize(self: VEC) -> VEC:
        try:
            return super().normalize()
        except ValueError:
            return VEC(0, 0)

WIDTH, HEIGHT = 1024, 768
SIZE = VEC(WIDTH, HEIGHT)
CENTER = SIZE // 2
FPS = 1000
PIXEL_SIZE = 4

COLORKEY = (0, 255, 255)