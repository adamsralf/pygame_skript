import os
from time import time
from typing import Dict

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1220, 1002)
    FPS = 60
    DELTATIME = 1.0/FPS
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")
    CAPTION = 'Fingerübung "Bubbles"'

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.PATH["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.PATH["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.PATH["sound"], filename)

class Background(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = Settings.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Settings.WINDOW.size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)    # Holt sich screen§\label{srcBubble0101}§


class Game:

    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption(Settings.CAPTION)
        self._clock = pygame.time.Clock()
        self._background = Background()
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False

    def draw(self) -> None:
        self._background.draw()
        pygame.display.update()

    def update(self) -> None:
        pass

    def run(self) -> None:
        time_previous = time()
        self._running = True
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
