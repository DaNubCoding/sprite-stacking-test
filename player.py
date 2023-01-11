from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scene import Scene

from math import atan2, degrees
from pygame.locals import *
import pygame

from stacked_sprite import StackedSprite
from sprite import Layers
from constants import *
from utils import *

class Player(StackedSprite):
    _res = "car.png"
    _size = VEC(10, 16)
    _frames = 9
    _pixel = 6

    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.PLAYER, CENTER, 0)
        self.vel = VEC(0, 0)

        self.acc = 1000
        self.friction = 500
        self.max_speed = 500

    def update(self) -> None:
        m_pos = VEC(pygame.mouse.get_pos())
        self.rot = degrees(atan2(*(CENTER - m_pos)))

        if self.manager.key_presses[K_w]:
            self.vel += (m_pos - CENTER).normalize() * self.acc * self.manager.dt

        # Apply friction
        dec = self.vel.normalize() * self.friction * self.manager.dt
        self.vel -= min(self.vel.x, dec.x, key=abs), min(self.vel.y, dec.y, key=abs)

        if self.vel.magnitude() > self.max_speed:
            self.vel.clamp_magnitude_ip(self.max_speed)

        self.pos += self.vel * self.manager.dt