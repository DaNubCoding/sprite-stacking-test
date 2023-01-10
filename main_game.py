from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import Manager

import pygame

from camera import Camera
from player import Player
from scene import Scene
from constants import *

class MainGame(Scene):
    def __init__(self, manager: Manager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

        Player.create_cache()
        self.player = Player(self)
        self.camera = Camera(self.player)

    def update(self) -> None:
        self.camera.update()
        super().update()

    def draw(self) -> None:
        self.manager.screen.fill((30, 30, 30))
        for i in range(50):
            pygame.draw.rect(self.manager.screen, (0, 255, 0), (VEC(500, i * 200) - self.camera.pos, (50, 50)))
        super().draw()