import os

import pygame
import pygame.time


class Settings:
    window = {'width': 120, 'height': 650}
    fps = 300                                            # 10 30 60 120 240 300 600
    limit = 500
    deltatime = 1.0/fps

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
    defender_pos = pygame.math.Vector2(defender_rect.left, defender_rect.top)    # float§\label{srcInvader05h01}§
    defender_speed = 600
    defender_direction_v = -1

    start_time = pygame.time.get_ticks()
    running = True
    while running:
        if pygame.time.get_ticks() > start_time + Settings.limit:
            defender_speed = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_pos[1] += defender_direction_v * defender_speed * Settings.deltatime
        defender_rect.top = round(defender_pos[1])                  # Runden§\label{srcInvader05h02}§
        if defender_rect.bottom >= Settings.window['height']:
            defender_direction_v *= -1
        elif defender_rect.top <= 0:
            defender_direction_v *= -1

        # Draw
        screen.fill("white")
        pygame.draw.line(screen, "red", (0, 315), (Settings.window['width'], 315), 2)
        screen.blit(defender_image, defender_rect)
        pygame.display.flip()
        Settings.deltatime = clock.tick(Settings.fps) / 1000.0
    print(f"top={defender_rect.top}")

    pygame.quit()


if __name__ == '__main__':
    main()
