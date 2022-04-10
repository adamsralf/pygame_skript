import os
from time import time
from typing import Any

import pygame


class Settings:
    window = {'width': 150, 'height': 150}
    fps = 60
    deltatime = 1.0 / fps

    @staticmethod
    def window_dim():
        return (Settings.window['width'], Settings.window['height'])


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect : pygame.rect.Rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2) # §\label{srcTastatur0001}§
        self.position : pygame.math.Vector2 = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.direction : pygame.math.Vector2 = pygame.math.Vector2(1, 0)   # 2 Dimensionen §\label{srcTastatur0002}§
        self.change_direction("right")
        self.change_direction("start")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.position = self.position + self.speed * Settings.deltatime * self.direction
                self.rect.left, self.rect.top = round(self.position.x) , round(self.position.y)
            elif kwargs["action"] == "switch":
                self.direction *= -1
        elif "direction" in kwargs.keys():
            self.change_direction(kwargs["direction"])

    def change_direction(self, direction:str) -> None:
        if direction == "right":
            self.direction.x, self.direction.y  = (1, 0)
        elif direction == "left":
            self.direction.x, self.direction.y = (-1, 0)
        elif direction == "up":
            self.direction.x, self.direction.y = (0, -1)
        elif direction == "down":
            self.direction.x, self.direction.y = (0, 1)
        elif direction == "stop":
            self.speed = 0
        elif direction == "start":
            self.speed = 100



class Border(pygame.sprite.Sprite):

    def __init__(self, whichone:str) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick1.png").convert_alpha()
        if whichone == 'right':
            self.image = pygame.transform.scale(self.image, (10, Settings.window['height']))
            self.rect = self.image.get_rect()
            self.rect.left = Settings.window['width'] - self.rect.width
        elif whichone == 'left':
            self.image = pygame.transform.scale(self.image, (10, Settings.window['height']))
            self.rect = self.image.get_rect()
            self.rect.left = 0
        elif whichone == 'top':
            self.image = pygame.transform.scale(self.image, (Settings.window['width'], 10))
            self.rect = self.image.get_rect()
            self.rect.top = 0
        elif whichone == 'down':
            self.image = pygame.transform.scale(self.image, (Settings.window['width'], 10))
            self.rect = self.image.get_rect()
            self.rect.bottom = Settings.window['height']


class Game(object):

    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.window_dim())
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
            self.clock.tick(Settings.fps)
            time_current = time()
            Settings.deltatime = time_current - time_previous
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
