import pygame

pygame.display.set_mode((50, 50))

spritesheets = {
    "car.png": pygame.image.load("car.png").convert(),
    "building.png": pygame.image.load("building.png").convert(),
    "tree.png": pygame.image.load("tree.png").convert()
}
for image in spritesheets.values():
    image.set_colorkey((0, 0, 0))

pygame.display.quit()