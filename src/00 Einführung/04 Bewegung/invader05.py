import os

import pygame


class Settings:
    window = {'width': 600, 'height': 100}
    fps = 60

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
    defender_rect = defender_image.get_rect()               # Rect-Objekt §\label{srcInvader0501}§
    defender_rect.centerx = Settings.window['width'] // 2   # Nicht nur left §\label{srcInvader0502}§
    defender_rect.bottom = Settings.window['height'] - 5    # Nicht nur top §\label{srcInvader0503}§

    running = True
    while running:
        clock.tick(Settings.fps)
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
