import os
from time import time

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))
    FPS = 60
    DELTATIME = 1.0 / FPS


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.centerx = Settings.WINDOW.centerx
        self.rect.bottom = Settings.WINDOW.bottom - 5
        self.speed = 300

    def update(self) -> None:
        self.rect.move_ip(self.speed * Settings.DELTATIME, 0)   # §\label{srcInvader06b01}§

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None:
        self.speed *= -1


class Border(pygame.sprite.Sprite):

    def __init__(self, leftright: str) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, Settings.WINDOW.width))
        self.rect = self.image.get_rect()
        if leftright == 'right':
            self.rect.left = Settings.WINDOW.width - self.rect.width

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.WINDOW.size)
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

        clock.tick(Settings.FPS)
        time_current = time()
        Settings.DELTATIME = time_current - time_previous
        time_previous = time_current

    pygame.quit()


if __name__ == '__main__':
    main()
