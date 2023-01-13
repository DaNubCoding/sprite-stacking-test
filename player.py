from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scene import Scene

from pygame.locals import *
from math import tan
import pygame

from stacked_sprite import StackedSprite
from sprite import Layers
from constants import *
from utils import *

class Player(StackedSprite):
    _res = "car.png"
    _size = VEC(10, 16)
    _frames = 9
    _pixel = 4

    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.WORLD, (0, 0), 0)
        self.vel = VEC(0, 0)
        self.backing = False

        self.acc = 1000
        self.friction = 500
        self.forward_speed = 500
        self.backward_speed = 200

    def update(self) -> None:
        if self.manager.key_presses[K_a]:
            self.rot += 100 * self.manager.dt
        if self.manager.key_presses[K_d]:
            self.rot -= 100 * self.manager.dt
        if self.manager.key_presses[K_w]:
            self.vel += VEC(0, -1).scale_to_length(self.acc).rotate(-self.rot) * self.manager.dt
            self.backing = False
        if self.manager.key_presses[K_s]:
            self.vel += VEC(0, 1).scale_to_length(self.acc).rotate(-self.rot) * self.manager.dt
            self.backing = True

        dec = self.vel.normalize() * self.friction * self.manager.dt
        self.vel -= min(self.vel.x, dec.x, key=abs), min(self.vel.y, dec.y, key=abs)

        if self.vel.magnitude() > self.forward_speed:
            self.vel.clamp_magnitude_ip(self.forward_speed)
        if self.backing and self.vel.magnitude():
            self.vel.clamp_magnitude_ip(self.backward_speed)

        self.pos += self.vel * self.manager.dt

        self.y_sort = self.screen_pos.y + self.image.get_height() * 0.8