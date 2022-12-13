import os

import pygame


class Settings:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    FPS = 60


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Bitmaps laden und ausgeben")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert()  # konvertieren §\label{srcInvader0201}§
    defender_image = pygame.transform.scale(defender_image, (30, 30))      # skalieren §\label{srcInvader0202}§

    enemy_image = pygame.image.load("images/alienbig0101.png").convert()
    enemy_image = pygame.transform.scale(enemy_image, (50, 45))

    running = True
    while running:
        clock.tick(Settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        screen.blit(enemy_image, (10, 10))
        screen.blit(defender_image, (10, 80))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
