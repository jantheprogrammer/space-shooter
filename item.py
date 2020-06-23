from ship import Ship
import pygame
import os


# Load images
MED_KIT = pygame.image.load(os.path.join("assets", "med_kit.png"))


class Item:
    ITEM_MAP = {
        "med_kit": MED_KIT,
    }

    def __init__(self, x, y, item):
        super().__init__(x, y)
        self.ship_img, self.laser_img = self.ITEM_MAP(item)
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 1

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def move(self):
        self.y += self.vel

