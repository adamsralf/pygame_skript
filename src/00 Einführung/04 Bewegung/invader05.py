import os

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))           # Rect-Objekt §\label{srcInvader0504a}§
    FPS = 60


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.WINDOW.size)  # Zugriff auf ein Rect-Attribut §\label{srcInvader0504b}§
    pygame.display.set_caption("Bewegung")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()               # Rect-Objekt §\label{srcInvader0501}§
    defender_rect.centerx = Settings.WINDOW.centerx         # Nicht nur left §\label{srcInvader0502}§
    defender_rect.bottom = Settings.WINDOW.height - 5       # Nicht nur top §\label{srcInvader0503}§

    running = True
    while running:
        clock.tick(Settings.FPS)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)          # blit kann auch rect §\label{srcInvader0504}§
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
