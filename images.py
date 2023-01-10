import pygame

pygame.display.set_mode((50, 50))

spritesheets = {
    "car.png": pygame.image.load("car.png").convert()
}
for image in spritesheets.values():
    image.set_colorkey((0, 0, 0))

pygame.display.quit()