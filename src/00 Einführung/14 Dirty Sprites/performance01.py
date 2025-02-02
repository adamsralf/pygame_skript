import os
import time
from random import randint
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT

from mytools import Timer
from settings import Settings


class Tile(pygame.sprite.DirtySprite):
    def __init__(self, topleft: tuple[int, int]) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, Settings.size, Settings.size)
        self.rect.topleft = topleft
        self.image = pygame.surface.Surface(self.rect.size)
        self.image.fill("white")
        self._timer: Timer
        self._status = 0
        self._counter = 1
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self._counter < 0:
            self.kill()
        if "action" in kwargs.keys():
            if kwargs["action"] == "switch" and self._status == 0:
                self._timer = Timer(100, False)
                self.image.fill("red")
                self._status = 1
                self.dirty = 1
                self._counter -= 1
        if self._status == 1 and self._timer.is_next_stop_reached():
            self.image.fill("white")
            self._status = 0
            self.dirty = 1


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Simple mit Dirty Sprites")
        self._clock = pygame.time.Clock()
        self._all_tiles = pygame.sprite.LayeredDirty()
        self.create_playground()
        self._background_image = pygame.image.load(Settings.get_image("background.png"))
        self._background_image = pygame.transform.scale(self._background_image, (Settings.WINDOW.size))
        self._running = True
        self._all_tiles.clear(self._screen, self._background_image)
        self._all_tiles.set_timing_threshold(1000 / Settings.FPS)
        self._performance: list[float] = []

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False

    def draw(self) -> None:
        areas = self._all_tiles.draw(self._screen)
        pygame.display.update(areas)

    def update(self):
        if len(self._all_tiles) == 0:
            self._running = False
        else:
            index = randint(0, len(self._all_tiles) - 1)
            self._all_tiles.sprites()[index].update(action="switch")

    def run(self):
        self._running = True
        while self._running:
            self._clock.tick(Settings.FPS)
            start = time.perf_counter()
            self.watch_for_events()
            self.update()
            self.draw()
            duration = time.perf_counter() - start
            self._performance.append(duration)
        with open(Settings.get_file(f"perf1_{Settings.size}_{Settings.number}.txt"), "w") as datei:
            for item in self._performance:
                datei.write(f"{item}\n")

        pygame.quit()

    def create_playground(self) -> None:
        for _ in range(Settings.number):
            tries = 10
            while tries > 0:
                left = randint(0, Settings.WINDOW.width - Settings.size)
                top = randint(0, Settings.WINDOW.height - Settings.size)
                tile = Tile((left, top))
                collided = pygame.sprite.spritecollide(tile, self._all_tiles, False)
                if len(collided) == 0:
                    self._all_tiles.add(tile)
                    break
                tries -= 1


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    Game().run()


if __name__ == "__main__":
    main()
