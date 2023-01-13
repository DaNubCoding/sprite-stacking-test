from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager import Manager

from typing import Type

from sprite import SpriteManager

class Scene:
    def __init__(self, manager: Manager, previous_scene: Scene, sprite_manager: Type[SpriteManager] = SpriteManager) -> None:
        self.manager = manager
        self.previous_scene = previous_scene
        self.sprite_manager = sprite_manager(self)
        self.running = True

    def update(self) -> None:
        self.sprite_manager.update()

    def draw(self) -> None:
        self.sprite_manager.draw()