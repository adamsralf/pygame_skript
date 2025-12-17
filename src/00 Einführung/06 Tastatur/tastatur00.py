from time import time
from typing import Any

import pygame


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (300, 300))
    FPS = 60
    DELTATIME = 1.0 / FPS
    DIRECTIONS = {
        "right": pygame.math.Vector2(1, 0),
        "left": pygame.math.Vector2(-1, 0),
        "up": pygame.math.Vector2(0, -1),
        "down": pygame.math.Vector2(0, 1),
    }


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.center = Settings.WINDOW.center       # §\label{srcTastatur0001}§
        self.direction = Settings.DIRECTIONS["right"]   # 2 dimensions§\label{srcTastatur0002}§
        self.change_direction("right")
        self.change_direction("start")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.rect.move_ip(self.speed * Settings.DELTATIME * self.direction)
                self.rect.clamp_ip(Settings.WINDOW)     # Keep inside window§\label{srcTastatur0008}§
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


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=Settings.WINDOW.size, title="Keyboard", position=(10, 50))
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.defender = pygame.sprite.GroupSingle(Defender())
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
            elif event.type == pygame.KEYDOWN:          # Key pressed§\label{srcTastatur0003}§
                if event.key == pygame.K_ESCAPE:        #§\label{srcTastatur0004}§
                    self.running = False
                elif event.key == pygame.K_RIGHT:       # Arrows§\label{srcTastatur0005}§
                    self.defender.update(direction="right")
                elif event.key == pygame.K_LEFT:
                    self.defender.update(direction="left")
                elif event.key == pygame.K_UP:
                    self.defender.update(direction="up")
                elif event.key == pygame.K_DOWN:
                    self.defender.update(direction="down")
                elif event.key == pygame.K_SPACE:       # Space key§\label{srcTastatur0006}§
                    self.defender.update(action="switch")
                elif event.key == pygame.K_p:
                    if event.mod & pygame.KMOD_LSHIFT:  # Shift key§\label{srcTastatur0007}§
                        self.defender.update(direction="stop")
                    else:
                        self.defender.update(direction="start")

    def update(self) -> None:
        self.defender.update(action="move")

    def draw(self) -> None:
        self.screen.fill("white")
        self.defender.draw(self.screen)
        self.window.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
