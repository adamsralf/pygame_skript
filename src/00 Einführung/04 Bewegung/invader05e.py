import os

import pygame
import pygame.time


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (120, 650))
    FPS = 600  # 10 30 60 120 240 300 600 §\label{srcInvader05e01}§
    LIMIT = 60


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
    defender_rect.bottom = Settings.WINDOW.bottom - 5
    defender_speed = 2
    defender_direction_v = -1

    start_time = pygame.time.get_ticks()  # Startzeit der Bewegung  §\label{srcInvader05e02}§
    running = True
    while running:
        if pygame.time.get_ticks() > start_time + Settings.LIMIT:  # Fertig?§\label{srcInvader05e04}§
            defender_speed = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.top += defender_direction_v * defender_speed  # Neue Höhe§\label{srcInvader05e03}§
        if defender_rect.bottom >= Settings.WINDOW.bottom:
            defender_direction_v *= -1
        elif defender_rect.top <= 0:
            defender_direction_v *= -1

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        pygame.display.flip()
        clock.tick(Settings.FPS)
    print(f"top={defender_rect.top}")

    pygame.quit()


if __name__ == '__main__':
    main()
