from __future__ import annotations

from pygame._sdl2.video import Window, Renderer, Texture
from typing import Sequence, Optional, Iterable
from fishhook import hook
import pygame

from constants import *

RectValue = pygame.Rect | tuple[int, int, int, int] | Sequence[int]

@hook(Texture)
def blit(self: Texture, dest: tuple[int, int], srcrect: Optional[RectValue] = None, angle: int = 0, origin: Optional[Iterable[int]] = None, flip_x: bool = False, flip_y: bool = False) -> None:
    return self.draw(srcrect, self.get_rect(topleft=dest), angle, origin, flip_x, flip_y)

__blit = Renderer.blit
@hook(Renderer)
def blit(self: Renderer, source: Texture, dest: tuple[float, float] | VEC, area: pygame.Rect | tuple[int, int, int, int] = None, special_flags: int = 0) -> pygame.Rect:
    return __blit(self, source, source.get_rect(topleft=dest), area, special_flags)