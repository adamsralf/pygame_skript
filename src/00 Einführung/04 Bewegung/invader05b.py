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
    defender_speed = 2                                      # Geschwindigkeit §\label{srcInvader0505}§
    defender_direction_h = 1                                # Richtung §\label{srcInvader0506}§

    running = True
    while running:
        clock.tick(Settings.FPS)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.left += defender_direction_h * defender_speed  # Flexibler §\label{srcInvader0507}§

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
