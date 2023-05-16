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
        self.rect.move_ip(self.speed * Settings.DELTATIME, 0)

    def change_direction(self) -> None:
        self.speed *= -1


class Border(pygame.sprite.Sprite):

    def __init__(self, leftright: str) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, Settings.WINDOW.height))
        self.rect = self.image.get_rect()
        if leftright == 'right':
            self.rect.right = Settings.WINDOW.right


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode(Settings.WINDOW.size)
    pygame.display.set_caption("Sprite")
    clock = pygame.time.Clock()
    defender = pygame.sprite.GroupSingle(Defender())
    all_border = pygame.sprite.Group()
    all_border.add(Border('left'))
    all_border.add(Border('right'))

    time_previous = time()
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        if pygame.sprite.spritecollide(defender.sprite, all_border, False):  # ! §\label{srcInvader06c01}§
            defender.sprite.change_direction()  # §\label{srcInvader06c02}§
        defender.update()

        # Draw
        screen.fill((255, 255, 255))
        defender.draw(screen)
        all_border.draw(screen)                 # Mit einem Rutsch §\label{srcInvader06c03}§
        pygame.display.flip()

        clock.tick(Settings.FPS)
        time_current = time()
        Settings.DELTATIME = time_current - time_previous
        time_previous = time_current
    pygame.quit()


if __name__ == '__main__':
    main()
