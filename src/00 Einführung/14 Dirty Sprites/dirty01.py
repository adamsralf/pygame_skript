import os
from random import randint
from typing import Any, Tuple

import pygame
from pygame import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT

from mytools import Timer
from settings import Settings


class Tile(pygame.sprite.DirtySprite):  # Neue Super-Klasse§\label{srcDirty0100}§
    def __init__(self, topleft: tuple[int, int]) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, Settings.size, Settings.size)
        self.rect.topleft = topleft
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        self.image.fill("white")
        self._timer: Timer
        self._status = 0
        self.dirty = 1  # Erstmaliges Zeichnen§\label{srcDirty0101}§

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "switch" and self._status == 0:
                self._timer = Timer(500, False)
                self.image.fill("red")
                self._status = 1
                self.dirty = 1  # Muss neu gezeichnet werden§\label{srcDirty0102}§
            if kwargs["action"] == "kill" and self._status == 1:
                self.kill()
        if self._status == 1 and self._timer.is_next_stop_reached():
            self.image.fill("white")
            self._status = 0
            self.dirty = 1  # Muss neu gezeichnet werden§\label{srcDirty0103}§


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Dirty Sprites Demo")
        self._clock = pygame.time.Clock()
        self._background_image = pygame.image.load(Settings.get_image("background.png"))
        self._background_image = pygame.transform.scale(self._background_image, (Settings.WINDOW.size))
        self._all_tiles = pygame.sprite.LayeredDirty()  # Gruppenklasse für DirtySprite§\label{srcDirty0104}§
        self.create_playground()
        self._timer = Timer(1000, False)
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.klick(pygame.mouse.get_pos())

    def draw(self) -> None:
        self._screen.blit(self._background_image, (0, 0))
        self._all_tiles.draw(self._screen)
        pygame.display.flip()

    def update(self):
        if len(self._all_tiles) == 0:
            self._running = False
        if self._timer.is_next_stop_reached():
            index = randint(0, len(self._all_tiles) - 1)
            self._all_tiles.sprites()[index].update(action="switch")

    def run(self):
        self._running = True
        while self._running:
            self._clock.tick(Settings.FPS)
            self.watch_for_events()
            self.update()
            self.draw()

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

    def klick(self, mousepos: Tuple[int, int]) -> None:
        for tile in self._all_tiles.sprites():
            if tile.rect.collidepoint(mousepos):
                tile.update(action="kill")


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    Game().run()


if __name__ == "__main__":
    main()
