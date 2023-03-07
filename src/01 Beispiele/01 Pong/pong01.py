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


class Game:
    def __init__(self):
        pygame.init()
        self._display = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("My Kind of Pong")
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
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

    def draw(self):
        self._background.draw(self._display)
        pygame.display.update()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
