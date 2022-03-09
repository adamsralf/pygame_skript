import os
import time
from random import randint
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, K_LEFT, K_RIGHT, KEYDOWN, MOUSEBUTTONDOWN, QUIT

from mytools import Timer
from settings import Settings


class Tile(pygame.sprite.DirtySprite):
    def __init__(self, color: tuple[int, int, int], topleft: tuple[int, int]) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, Settings.size, Settings.size)
        self.rect.topleft = topleft
        self.color = color
        self.image: pygame.surface.Surface = pygame.surface.Surface((self.rect.width, self.rect.height))
        self.image.fill(color)
        self.timer: Timer
        self.status = 0
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "switch" and self.status == 0:
                self.timer = Timer(500, False)
                self.image.fill((255, 0, 0))
                self.status = 1
                self.dirty = 1
            if kwargs["action"] == "kill" and self.status == 1:
                self.kill()
        if self.status == 1 and self.timer.is_next_stop_reached():
            self.image.fill(self.color)
            self.status = 0
            self.dirty = 1


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption("Simple mit Dirty Sprites")
        self.clock = pygame.time.Clock()
        self.all_tiles = pygame.sprite.LayeredDirty()
        self.create_playground()
        self.background_image = pygame.image.load(Settings.get_image("background.png"))
        self.background_image = pygame.transform.scale(self.background_image, (Settings.get_dim()))
        self.timer = Timer(1000, False)
        self.running = True
        self.all_tiles.clear(self.screen, self.background_image)
        self.all_tiles.set_timing_treshold(1000 / Settings.fps)

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_LEFT:
                    pass
                elif event.key == K_RIGHT:
                    pass
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.klick(pygame.mouse.get_pos())

    def draw(self) -> None:
        areas = self.all_tiles.draw(self.screen)
        pygame.display.update(areas)

    def update(self):
        if len(self.all_tiles) == 0:
            self.running = False
        if self.timer.is_next_stop_reached():
            index = randint(0, len(self.all_tiles) - 1)
            self.all_tiles.sprites()[index].update(action="switch")

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        pygame.quit()

    def create_playground(self) -> None:
        for _ in range(Settings.number):
            ok = False
            while not ok:
                x = randint(0, Settings.window.width - Settings.size)
                y = randint(0, Settings.window.height - Settings.size)
                t = Tile((255, 255, 255), (x, y))
                l = pygame.sprite.spritecollide(t, self.all_tiles, False)
                if l:
                    ok = False
                else:
                    ok = True
            self.all_tiles.add(t)

    def klick(self, mousepos: Tuple[int, int]) -> None:
        for tile in self.all_tiles.sprites():
            if tile.rect.collidepoint(mousepos):
                tile.update(action="kill")


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
