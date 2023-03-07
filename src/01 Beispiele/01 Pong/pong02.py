from time import time
from typing import Any, Tuple

import pygame


class Settings:
    WINDOW: pygame.rect.Rect = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    DELTATIME = 1.0/FPS


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
        self.rect = pygame.Rect(0, 0, 15, Settings.WINDOW.height//10)   # Größe §\label{srcPong0201}§
        y = Settings.WINDOW.centery                                     # Position §\label{srcPong0202}§
        if player == "left":
            x = 50
        else:
            x = Settings.WINDOW.right - 50
        self.rect.center = (x, y)
        self._speed = Settings.WINDOW.height // 2                       # Geschwindigkeit§\label{srcPong0206}§
        self._direction = 0
        self.image = pygame.surface.Surface(self.rect.size)             # Surface §\label{srcPong0203}§
        self.image.fill("yellow")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":                              # Postionsänderung §\label{srcPong0204}§
                self._move()
            elif kwargs["action"] == "up":                              # Bewegungsrichtung §\label{srcPong0205}§
                self._direction = -1
            elif kwargs["action"] == "down":
                self._direction = 1
            elif kwargs["action"] == "halt":
                self._direction = 0
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        self.rect.centery += self._speed * self._direction * Settings.DELTATIME   # §\label{srcPong0207}§
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.WINDOW.bottom:
            self.rect.bottom = Settings.WINDOW.bottom


class Game:
    def __init__(self):
        pygame.init()
        self._display = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("My Kind of Pong")
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
        self._all_sprites = pygame.sprite.Group()                       # Schläger §\label{srcPong0208}§
        self._paddle1 = Paddle("left", self._all_sprites)
        self._paddle2 = Paddle("right", self._all_sprites)
        self._running = True

    def run(self):
        time_previous = time()
        while self._running:
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def update(self):
        self.watch_for_events()
        self._all_sprites.update(action="move")                         # Bewegung §\label{srcPong0209}§

    def draw(self):
        self._background.draw(self._display)
        self._all_sprites.draw(self._display)                           # Ausgabe §\label{srcPong0210}§
        pygame.display.update()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_UP:                          # Schlägerbewegung §\label{srcPong0211}§
                    self._paddle2.update(action="up")
                elif event.key == pygame.K_DOWN:
                    self._paddle2.update(action="down")
                elif event.key == pygame.K_w:
                    self._paddle1.update(action="up")
                elif event.key == pygame.K_s:
                    self._paddle1.update(action="down")
            elif event.type == pygame.KEYUP:                            # Schlägerstopp §\label{srcPong0212}§
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self._paddle2.update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self._paddle1.update(action="halt")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
