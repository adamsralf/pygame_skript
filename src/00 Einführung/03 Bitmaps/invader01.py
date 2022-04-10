import os

import pygame


class Settings:
    window_width = 600
    window_height = 400
    fps = 60


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
    pygame.display.set_caption("Bitmaps laden und ausgeben")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png")     # Bitmap laden §\label{srcInvader0101}§
    enemy_image = pygame.image.load("images/alienbig0101.png")

    running = True
    while running:
        clock.tick(Settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        screen.blit(enemy_image, (10, 10))                          # Bitmap ausgeben §\label{srcInvader0102}§
        screen.blit(defender_image, (10, 80))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
