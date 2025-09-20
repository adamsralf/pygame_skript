import os
from random import randint
from typing import Any, Tuple

import pygame
from pygame import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT

from mytools import Timer
from settings import Settings


class Tile(pygame.sprite.Sprite):
    def __init__(self, topleft: Tuple[int, int]) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, Settings.size, Settings.size)
        self.rect.topleft = topleft
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        self.image.fill("white")  # Vordefinierte Farbnamen§\label{srcDirty0001}§
        self.timer: Timer
        self.status = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "switch" and self.status == 0:
                self.timer = Timer(500, False)
                self.image.fill("red")  # Vordefinierte Farbnamen§\label{srcDirty0002}§
                self.status = 1
            if kwargs["action"] == "kill" and self.status == 1:
                self.kill()
        if self.status == 1 and self.timer.is_next_stop_reached():
            self.image.fill("white")
            self.status = 0


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Dirty Sprites Demo")
        self.clock = pygame.time.Clock()
        self.all_tiles = pygame.sprite.Group()
        self.create_playground()
        self.background_image = pygame.image.load(Settings.get_image("background.png"))
        self.background_image = pygame.transform.scale(self.background_image, (Settings.WINDOW.size))
        self.timer = Timer(1000, False)
        self.running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.klick(pygame.mouse.get_pos())

    def draw(self) -> None:
        self.screen.blit(self.background_image, (0, 0))
        self.all_tiles.draw(self.screen)
        pygame.display.flip()

    def update(self):
        if len(self.all_tiles) == 0:
            self.running = False
        if self.timer.is_next_stop_reached():
            index = randint(0, len(self.all_tiles) - 1)
            self.all_tiles.sprites()[index].update(action="switch")

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(Settings.FPS)
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
                collided = pygame.sprite.spritecollide(tile, self.all_tiles, False)
                if len(collided) == 0:
                    self.all_tiles.add(tile)
                    break
                tries -= 1

    def klick(self, mousepos: Tuple[int, int]) -> None:
        for tile in self.all_tiles.sprites():
            if tile.rect.collidepoint(mousepos):
                tile.update(action="kill")


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    Game().run()


if __name__ == "__main__":
    main()
