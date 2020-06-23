import pygame
import os
import random

from player import Player
from enemy import Enemy, Boss
from utils import collide
from consts import WIDTH, HEIGHT, BLACK

pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    items = []
    wave_length = 5

    laser_vel = 8

    player = Player(round(WIDTH/2)-40, HEIGHT - 100)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    boss_spawned = True

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, BLACK)
        level_label = main_font.render(f"Level: {level}", 1, BLACK)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # draw enemies ship
        for en in enemies:
            en.draw(WIN)

        # draw player ship
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, BLACK)
            WIN.blit(lost_label, (round(WIDTH / 2 - lost_label.get_width() / 2), 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            if boss_spawned is True:
                level += 1
                wave_length += 5
                boss_spawned = False
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),
                                  random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
            else:
                boss = Boss(round(WIDTH/2) - 40, -100, level)
                enemies.append(boss)
                boss_spawned = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # player control
        keys = pygame.key.get_pressed()
        player.move(keys)

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, BLACK)
        WIN.blit(title_label, (round(WIDTH / 2 - title_label.get_width() / 2), 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()

# TODO implement healing kit from boss
# TODO give double laser to boss
# TODO do not spawn enemies on top of each other

