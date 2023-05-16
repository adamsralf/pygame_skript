import os

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))
    FPS = 60


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.WINDOW.size)
    pygame.display.set_caption("Bewegung")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()
    defender_rect.centerx = Settings.WINDOW.centerx
    defender_rect.bottom = Settings.WINDOW.height - 5

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.left = defender_rect.left + 1

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)          # blit kann auch rect §\label{srcInvader0504}§
        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
