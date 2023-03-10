from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scene import Scene

from pygame.locals import *
import pygame
import time

from sprite import VisibleSprite, Layers
from images import spritesheets
from constants import *
from utils import *

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

        edges = [{side: pygame.Surface((images[i].get_size())) for side in ["left", "right", "top", "bottom"]} for i in range(cls._frames)]
        for i, image in enumerate(images):
            width, height = image.get_size()
            mask = pygame.mask.from_surface(image)
            for x, y in range_2d(width, height):
                if not mask.get_at((x, y)): continue
                for side, func in get_side_pixel.items():
                    if func(mask, x, y, width, height): continue
                    edges[i][side].set_at((x, y), transform_color(lambda x: x * (1 - SHADING[side]), image.get_at((x, y))))
                    break

        for rot in range(360):
            rotated_size = VEC(pygame.transform.rotate(images[0], rot).get_size())
            surface = pygame.Surface((rotated_size.x, rotated_size.y + (cls._frames - 1) * cls._pixel), SRCALPHA)
            surface.fill(COLORKEY)
            cls._pivot_cache[rot] = VEC(surface.get_width() // 2, surface.get_height() - rotated_size.y // 2) + cls._pivot_offset.rotate(-rot) * cls._pixel
            for i, image in enumerate(images):
                shaded_image = image.copy()
                for side in visible_sides(rot):
                    shaded_image.blit(edges[i][side], (0, 0), special_flags=BLEND_RGB_SUB)
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