import os
from time import time
from typing import Any

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 100))
    FPS = 60
    DELTATIME = 1.0 / FPS
    DIRECTIONS = {"right": pygame.math.Vector2(1, 0), 
                  "left": pygame.math.Vector2(-1, 0), 
                  "up": pygame.math.Vector2(0, -1), 
                  "down": pygame.math.Vector2(0, 1)}


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.center = Settings.WINDOW.center  # §\label{srcTastatur0001}§
        self.direction = Settings.DIRECTIONS["right"]   # 2 Dimensionen §\label{srcTastatur0002}§
        self.change_direction("right")
        self.change_direction("start")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.rect.move_ip(self.speed * Settings.DELTATIME * self.direction)
            elif kwargs["action"] == "switch":
                self.direction *= -1
        elif "direction" in kwargs.keys():
            self.change_direction(kwargs["direction"])

    def change_direction(self, direction: str) -> None:
        if direction in Settings.DIRECTIONS.keys():
            self.direction = Settings.DIRECTIONS[direction]
        elif direction == "stop":
            self.speed = 0
        elif direction == "start":
            self.speed = 100


class Border(pygame.sprite.Sprite):

    def __init__(self, whichone: str) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick1.png").convert_alpha()
        if whichone == 'right':
            self.image = pygame.transform.scale(self.image, (10, Settings.WINDOW.height))
            self.rect = self.image.get_rect()
            self.rect.right = Settings.WINDOW.right
        elif whichone == 'left':
            self.image = pygame.transform.scale(self.image, (10, Settings.WINDOW.height))
            self.rect = self.image.get_rect()
            self.rect.left = Settings.WINDOW.left
        elif whichone == 'top':
            self.image = pygame.transform.scale(self.image, (Settings.WINDOW.width, 10))
            self.rect = self.image.get_rect()
            self.rect.top = Settings.WINDOW.top
        elif whichone == 'down':
            self.image = pygame.transform.scale(self.image, (Settings.WINDOW.width, 10))
            self.rect = self.image.get_rect()
            self.rect.bottom = Settings.WINDOW.bottom


class Game(object):

    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Sprite")
        self.clock = pygame.time.Clock()
        self.defender = pygame.sprite.GroupSingle(Defender())
        self.all_border = pygame.sprite.Group()
        self.all_border.add(Border('left'))
        self.all_border.add(Border('right'))
        self.all_border.add(Border('top'))
        self.all_border.add(Border('down'))
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:          # Taste drücken §\label{srcTastatur0003}§
                if event.key == pygame.K_ESCAPE:        # Boss-Taste §\label{srcTastatur0004}§
                    self.running = False
                elif event.key == pygame.K_RIGHT:       # Pfeiltasten §\label{srcTastatur0005}§
                    self.defender.update(direction="right")
                elif event.key == pygame.K_LEFT:
                    self.defender.update(direction="left")
                elif event.key == pygame.K_UP:
                    self.defender.update(direction="up")
                elif event.key == pygame.K_DOWN:
                    self.defender.update(direction="down")
                elif event.key == pygame.K_SPACE:       # Leerzeichen-Taste §\label{srcTastatur0006}§
                    self.defender.update(direction="stop")
                elif event.key == pygame.K_r:
                    if event.mod & pygame.KMOD_LSHIFT:  # Shift-Taste §\label{srcTastatur0007}§
                        self.defender.update(direction="stop")
                    else:
                        self.defender.update(direction="start")

    def update(self) -> None:
        if pygame.sprite.spritecollide(self.defender.sprite, self.all_border, False):
            self.defender.sprite.update(action="switch")
        self.defender.update(action="move")

    def draw(self) -> None:
        self.screen.fill("white")
        self.defender.draw(self.screen)
        self.all_border.draw(self.screen)
        pygame.display.flip()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
