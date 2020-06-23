import pygame
import os

from ship import Ship
from consts import WIDTH, HEIGHT, RED, GREEN

PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
PLAYER_SPACE_SHIP_RIGHT = pygame.image.load(os.path.join("assets", "pixel_ship_yellow_right.png"))
PLAYER_SPACE_SHIP_LEFT = pygame.image.load(os.path.join("assets", "pixel_ship_yellow_left.png"))
PLAYER_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))


class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, health=100)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = 100
        self.vel = 8
        self.dmg = 10

    def move(self, key):
        if key[pygame.K_a] and self.x - self.vel > 0:  # left
            self.ship_img = PLAYER_SPACE_SHIP_LEFT
            self.x -= self.vel
        elif key[pygame.K_d] and self.x + self.vel + self.get_width() < WIDTH:  # right
            self.ship_img = PLAYER_SPACE_SHIP_RIGHT
            self.x += self.vel
        else:
            self.ship_img = PLAYER_SPACE_SHIP

        if key[pygame.K_w] and self.y - self.vel > 0:  # up
            self.y -= self.vel
        if key[pygame.K_s] and self.y + self.vel + self.get_height() + 15 < HEIGHT:  # down
            self.y += self.vel
        if key[pygame.K_SPACE]:
            self.shoot()

    def move_lasers(self, vel, objs):
        self.cooling_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if obj.health - self.dmg <= 0:
                            objs.remove(obj)
                            if obj.__class__.__name__ == 'Boss':
                                pass
                        else:
                            obj.health -= self.dmg

                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN,
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))
