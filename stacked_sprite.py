from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scene import Scene

import pygame
import time

from sprite import VisibleSprite, Layers
from images import spritesheets
from constants import *

class CacheNotCreatedException(Exception):
    def __init__(self, cls) -> None:
        super().__init__()
        self.cls = cls

    def __str__(self) -> str:
        return f"Call 'create_cache' on class '{self.cls.__name__}' to initialize cache."

class StackedSprite(VisibleSprite):
    def __init__(self, scene: Scene, layer: Layers, pos: tuple[int, int], rot: int) -> None:
        super().__init__(scene, layer)
        self.cls = self.__class__
        try:
            self.cls._cache
        except AttributeError:
            raise CacheNotCreatedException(self.cls)

        self.pos = VEC(pos)
        self.rot = rot

    @classmethod
    def create_cache(cls) -> None:
        try:
            cls._res, cls._size, cls._frames, cls._pixel
        except AttributeError as error:
            raise NotImplementedError(f"Class attribute {error.name} is not defined for subclass '{cls.__name__}'.")

        start = time.time()

        cls._cache = {}
        images = [spritesheets[cls._res].subsurface(0, i * cls._size.y, cls._size.x, cls._size.y) for i in range(cls._frames)]
        for rot in range(360):
            rotated_size = VEC(pygame.transform.rotate(pygame.transform.scale_by(images[0], cls._pixel), rot).get_size())
            surface = pygame.Surface((rotated_size.x, rotated_size.y + (cls._frames - 1) * cls._pixel))
            surface.fill(COLORKEY)
            surface.set_colorkey(COLORKEY)
            for i, image in enumerate(images):
                image = pygame.transform.rotate(pygame.transform.scale_by(image, cls._pixel), rot)
                for j in range(0, cls._pixel):
                    surface.blit(image, (0, surface.get_height() - rotated_size.y - i * cls._pixel - j))
            cls._cache[rot] = surface

        print(f"Cache for '{cls.__name__}' created in {round(time.time() - start, 5)} seconds")

    def draw(self) -> None:
        self.image = self.cls._cache[int((self.rot - self.scene.camera.rot) % 360)]
        self.manager.screen.blit(self.image, (self.pos - self.scene.camera.pos).rotate(self.scene.camera.rot) - VEC(self.image.get_size()) // 2 + SIZE // 2)