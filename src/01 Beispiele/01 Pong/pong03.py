import random
from time import time
from typing import Any, Tuple

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    DELTATIME = 1.0/FPS
    POINTS = [0, 0]                                                     # Punktestand§\label{srcPong0300}§


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.surface.Surface(Settings.WINDOW.size)
        self.image.fill("black")
        for ypos in range(2, Settings.WINDOW.bottom, 10):
            pygame.draw.line(self.image, "white", (Settings.WINDOW.centerx, ypos), (Settings.WINDOW.centerx, ypos+5), 2)
        self.rect = self.image.get_rect()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, player: str, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 15, Settings.WINDOW.height//10)
        y = Settings.WINDOW.centery
        if player == "left":
            x = 50
        else:
            x = Settings.WINDOW.right - 50
        self.rect.center = (x, y)
        self._speed = Settings.WINDOW.height // 2
        self._direction = 0
        self.image = pygame.surface.Surface(self.rect.size)
        self.image.fill("yellow")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] == "up":
                self._direction = -1
            elif kwargs["action"] == "down":
                self._direction = 1
            elif kwargs["action"] == "halt":
                self._direction = 0
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        self.rect.centery += self._speed * self._direction * Settings.DELTATIME
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(Settings.WINDOW.bottom, self.rect.bottom)


class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 20, 20)                     # Größe§\label{srcPong0301}§
        self.image = pygame.surface.Surface(self.rect.size)
        pygame.draw.circle(self.image, "green", self.rect.center, self.rect.width//2)
        self._speed = Settings.WINDOW.width // 3                        # Geschwindigkeit§\label{srcPong0302}§
        self._speedxy = pygame.Vector2()
        self._service()                                                 # Aufschlag§\label{srcPong0303}§

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] == "hflip":
                self._horizontal_flip()
            elif kwargs["action"] == "vflip":
                self._vertical_flip()
            elif kwargs["action"] == "reset":
                self._service()
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        self.rect.move_ip(self._speedxy * Settings.DELTATIME)
        if self.rect.top <= 0:                             # Rändercheck§\label{srcPong0304}§
            self._vertical_flip()
            self.rect.top = 0
        elif self.rect.bottom >= Settings.WINDOW.bottom:
            self._vertical_flip()
            self.rect.bottom = Settings.WINDOW.bottom
        elif self.rect.right < 0:
            Settings.POINTS[1] += 1
            self._service()
        elif self.rect.left > Settings.WINDOW.right:
            Settings.POINTS[0] += 1
            self._service()

    def _service(self) -> None:
        self.rect.center = Settings.WINDOW.center
        self._speedxy = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])) * self._speed
        print(Settings.POINTS)                              # Provisorium§\label{srcPong0305}§

    def _horizontal_flip(self) -> None:
        self._speedxy.x *= -1

    def _vertical_flip(self) -> None:
        self._speedxy.y *= -1


class Game:
    def __init__(self):
        pygame.init()
        self._display = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("My Kind of Pong")
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
        self._all_sprites = pygame.sprite.Group()
        self._paddle1 = Paddle("left", self._all_sprites)
        self._paddle2 = Paddle("right", self._all_sprites)
        self._ball = Ball(self._all_sprites)
        self._running = True

    def run(self):
        time_previous = time()
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def update(self):
        self._all_sprites.update(action="move")

    def draw(self):
        self._background.draw(self._display)
        self._all_sprites.draw(self._display)
        pygame.display.update()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_UP:
                    self._paddle2.update(action="up")
                elif event.key == pygame.K_DOWN:
                    self._paddle2.update(action="down")
                elif event.key == pygame.K_w:
                    self._paddle1.update(action="up")
                elif event.key == pygame.K_s:
                    self._paddle1.update(action="down")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self._paddle2.update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self._paddle1.update(action="halt")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
