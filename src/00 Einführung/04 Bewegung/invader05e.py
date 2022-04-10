import os

import pygame
import pygame.time


class Settings:
    window = {'width': 120, 'height': 650}
    fps = 600  # 10 30 60 120 240 300 600 §\label{srcInvader05e01}§
    limit = 500

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Bewegung")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()
    defender_rect.centerx = Settings.window['width'] // 2
    defender_rect.bottom = Settings.window['height'] - 5
    defender_speed = 2
    defender_direction_v = -1

    start_time = pygame.time.get_ticks()  # Startzeit der Bewegung  §\label{srcInvader05e02}§
    running = True
    while running:
        if pygame.time.get_ticks() > start_time + Settings.limit:  # Fertig?§\label{srcInvader05e04}§
            defender_speed = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.top += defender_direction_v * defender_speed  # Neue Höhe§\label{srcInvader05e03}§
        if defender_rect.bottom >= Settings.window['height']:
            defender_direction_v *= -1
        elif defender_rect.top <= 0:
            defender_direction_v *= -1

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        pygame.display.flip()
        clock.tick(Settings.fps)
    print(f"top={defender_rect.top}")

    pygame.quit()


if __name__ == '__main__':
    main()
