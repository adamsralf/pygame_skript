from time import time

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 300))
    FPS = 60
    DELTATIME = 1.0 / FPS


class Game:

    def __init__(self) -> None:
        pygame.init()
        self._window = pygame.Window(size=Settings.WINDOW.size, title="Event (0)", position=pygame.WINDOWPOS_CENTERED)
        self._screen = self._window.get_surface()
        self._clock = pygame.time.Clock()
        self._running = True

    def run(self) -> None:
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

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            print(event)  # Eventinfo ausgeben§\label{srcEvents0001}§
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False

    def update(self):
        pass

    def draw(self) -> None:
        self._screen.fill((250, 250, 250))
        self._window.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
