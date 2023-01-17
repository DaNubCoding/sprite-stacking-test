from __future__ import annotations
from pygame.math import Vector2

class VEC(Vector2):
    def normalize(self: VEC) -> VEC:
        try:
            return super().normalize()
        except ValueError:
            return VEC(0, 0)

    def scale_to_length(self, value: float) -> None:
        super().scale_to_length(value)
        return self

WIDTH, HEIGHT = 1024, 576
SIZE = VEC(WIDTH, HEIGHT)
CENTER = SIZE // 2
FPS = 1000

COLORKEY = (0, 255, 255, 255)
# SHADING = {"left": 32, "top": 24, "bottom": 16, "right": 8}
SHADING = {"left": 0.7, "top": 0.78, "bottom": 0.86, "right": 0.94}