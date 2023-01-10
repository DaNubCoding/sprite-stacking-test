from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import Manager

from stacked_sprite import Car
from scene import Scene

class MainGame(Scene):
    def __init__(self, manager: Manager, previous_scene: Scene) -> None:
        super().__init__(manager, previous_scene)

        Car.create_cache()

        for _ in range(100):
            self.car = Car(self)

    def update(self) -> None:
        super().update()

    def draw(self) -> None:
        self.manager.screen.fill((30, 30, 30))
        super().draw()