from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scene import Scene

from pygame.locals import *
import itertools
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
            self.cls._cache, self.cls._pivot_cache
        except AttributeError:
            raise CacheNotCreatedException(self.cls)

        self.pos = VEC(pos)
        self.screen_pos = self.pos.copy()
        self.rot = rot
        self.y_sort = self.screen_pos.y
        self.image = self.cls._cache[int(self.rot)]

    @classmethod
    def create_cache(cls) -> None:
        try:
            cls._res, cls._size, cls._frames, cls._pixel, cls._pivot_offset
        except AttributeError as error:
            raise NotImplementedError(f"Class attribute {error.name} is not defined for subclass '{cls.__name__}'.")

        start = time.time()

        cls._pivot_cache, cls._cache = {}, {}
        images = [spritesheets[cls._res].subsurface(0, i * cls._size.y, cls._size.x, cls._size.y) for i in range(cls._frames)]
        for i, image in enumerate(images):
            image.set_colorkey(COLORKEY)
            images[i] = pygame.transform.scale_by(image, cls._pixel)

        edges = [{"left": [], "right": [], "top": [], "bottom": []} for _ in range(cls._frames)]
        for i, image in enumerate(images):
            width, height = image.get_size()
            for y in range(height):
                for x in range(width):
                    pixel = image.get_at((x, y))
                    left_pixel = image.get_at((x - 1, y)) if x > 0 else COLORKEY
                    right_pixel = image.get_at((x + 1, y)) if x < width - 1 else COLORKEY
                    top_pixel = image.get_at((x, y - 1)) if y > 0 else COLORKEY
                    bottom_pixel = image.get_at((x, y + 1)) if y < height - 1 else COLORKEY
                    if pixel == COLORKEY: continue
                    if left_pixel == COLORKEY:
                        edges[i]["left"].append((x, y))
                    elif right_pixel == COLORKEY:
                        edges[i]["right"].append((x, y))
                    elif top_pixel == COLORKEY:
                        edges[i]["top"].append((x, y))
                    elif bottom_pixel == COLORKEY:
                        edges[i]["bottom"].append((x, y))

        for rot in range(360):
            rotated_size = VEC(pygame.transform.rotate(images[0], rot).get_size())
            surface = pygame.Surface((rotated_size.x, rotated_size.y + (cls._frames - 1) * cls._pixel), SRCALPHA)
            surface.fill(COLORKEY)
            cls._pivot_cache[rot] = VEC(surface.get_width() // 2, surface.get_height() - rotated_size.y // 2) + cls._pivot_offset.rotate(-rot) * cls._pixel
            for i, image in enumerate(images.copy()):
                shaded_image = image.copy()
                for side in edges[i]:
                    for pos in edges[i][side]:
                        darkened_color = (color := image.get_at(pos))[0] * SHADING_PERC[side], color[1] * SHADING_PERC[side], color[2] * SHADING_PERC[side]
                        shaded_image.set_at(pos, darkened_color)
                rotated_image = pygame.transform.rotate(shaded_image, rot)
                for j in range(0, cls._pixel):
                    surface.blit(rotated_image, (0, surface.get_height() - rotated_size.y - i * cls._pixel - j))
            surface.set_colorkey(COLORKEY)
            cls._cache[rot] = surface.convert()

        print(f"Cache for '{cls.__name__}' created in {round(time.time() - start, 5)} seconds")

    def update(self) -> None:
        _, self.y_sort = (self.pos - self.scene.camera.pos).rotate(self.scene.camera.rot) + SIZE // 2

    def draw(self) -> None:
        self.image = self.cls._cache[screen_rot := int((self.rot - self.scene.camera.rot) % 360)]
        self.screen_pos = (self.pos - self.scene.camera.pos).rotate(self.scene.camera.rot) + SIZE // 2 - self.cls._pivot_cache[screen_rot]
        if not -self.image.get_width() < self.screen_pos.x < WIDTH or not -self.image.get_height() < self.screen_pos.y < HEIGHT: return
        self.manager.screen.blit(self.image, self.screen_pos)

        if self.manager.debug:
            pygame.draw.circle(self.manager.screen, (0, 255, 255), (self.pos - self.scene.camera.pos).rotate(self.scene.camera.rot) + SIZE // 2, 5)