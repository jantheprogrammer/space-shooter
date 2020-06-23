from ship import Ship
import pygame
import os

from consts import WIDTH, RED, GREEN

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
BOSS_SHIP = pygame.image.load(os.path.join("assets", "boss_ship.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
BOSS_LASER = pygame.image.load(os.path.join("assets", "boss_laser.png"))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 1

    def move(self):
        self.y += self.vel


class Boss(Ship):
    def __init__(self, x, y, level):
        super().__init__(x, y, health=100, cool_down=20)
        self.ship_img = BOSS_SHIP
        self.laser_img = BOSS_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 2 + level
        self.direction = 'down'
        self.max_health = 100

    def move(self):
        if self.direction == 'down':
            if self.y + self.vel <= 100:
                self.y += self.vel
            else:
                self.direction = 'left'

        if self.direction == 'left':
            if self.x - self.vel >= 0:
                self.x -= self.vel
            else:
                self.direction = 'right'

        if self.direction == 'right':
            if self.x + self.vel + self.get_width() <= WIDTH:
                self.x += self.vel
            else:
                self.direction = 'left'

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y - 20, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (self.x, self.y - 20, self.ship_img.get_width() * (self.health / self.max_health), 10))

