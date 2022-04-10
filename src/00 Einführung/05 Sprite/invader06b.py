import os
from time import time

import pygame


class Settings:
    window = {'width': 600, 'height': 100}
    fps = 60
    deltatime = 1.0 / fps

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image: pygame.surface.Surface = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] // 2
        self.rect.bottom = Settings.window['height'] - 5
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = pygame.math.Vector2(300, 0)

    def update(self) -> None:
        self.position = self.position + (self.speed * Settings.deltatime)
        self.rect.left = round(self.position.x)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None:
        self.speed.x *= -1


class Border(pygame.sprite.Sprite):

    def __init__(self, leftright: str) -> None:
        super().__init__()
        self.image: pygame.surface.Surface = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, Settings.window['height']))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        if leftright == 'right':
            self.rect.left = Settings.window['width'] - self.rect.width

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.window_dim())
    pygame.display.set_caption("Sprite")
    clock = pygame.time.Clock()
    defender = Defender()
    border_left = Border('left')
    border_right = Border('right')

    time_previous = time()
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        if pygame.sprite.collide_rect(defender, border_left):
            defender.change_direction()
        elif pygame.sprite.collide_rect(defender, border_right):
            defender.change_direction()
        defender.update()

        # Draw
        screen.fill((255, 255, 255))
        defender.draw(screen)
        border_left.draw(screen)
        border_right.draw(screen)
        pygame.display.flip()

        clock.tick(Settings.fps)
        time_current = time()
        Settings.deltatime = time_current - time_previous
        time_previous = time_current

    pygame.quit()


if __name__ == '__main__':
    main()
