from time import time
from typing import Tuple

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    DELTATIME = 1.0 / FPS


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.surface.Surface(Settings.WINDOW.size).convert()
        self.rect = self.image.get_rect()
        self.image.fill("darkred")
        self._paint_net()

    def _paint_net(self) -> None:
        net_rect = pygame.rect.Rect(0, 0, 0, 0)
        net_rect.centerx = Settings.WINDOW.centerx
        net_rect.top = 50
        net_rect.size = (3, 30)
        while net_rect.bottom < Settings.WINDOW.bottom:  # Netz als Folge von Rechtecken §\label{srcPong0101}§
            pygame.draw.rect(self.image, "grey", net_rect, 0)
            net_rect.move_ip(0, 40)


class Game:
    def __init__(self):
        self._window = pygame.Window(size=Settings.WINDOW.size, title="My Kind of Pong", position=pygame.WINDOWPOS_CENTERED)
        self._screen = self._window.get_surface()
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
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
        pass

    def draw(self):
        self._background.draw(self._screen)
        self._window.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False


def main():
    Game().run()


if __name__ == "__main__":
    main()
