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

class Building(StackedSprite):
    _res = "building.png"
    _size = VEC(11, 13)
    _frames = 11
    _pixel = 8

    def __init__(self, scene: Scene, pos: tuple[int, int], rot: int) -> None:
        super().__init__(scene, Layers.WORLD, pos, rot)