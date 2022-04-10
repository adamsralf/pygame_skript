import os
from time import time
from typing import Dict

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Background(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = Game.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Game.window.size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1

    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)    # Holt sich screen§\label{srcBubble0101}§


class Game:
    window = pygame.rect.Rect(0, 0, 1220, 1002)
    fps = 60
    deltatime = 1.0/fps
    path: Dict[str, str] = {}
    path["file"] = os.path.dirname(os.path.abspath(__file__))
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")
    caption = 'Fingerübung "Bubbles"'

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Game.path["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Game.path["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Game.path["sound"], filename)

    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Game.window.size)
        pygame.display.set_caption(Game.caption)
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
            self._clock.tick(Game.fps)
            time_current = time()
            Game.deltatime = time_current - time_previous
            time_previous = time_current
        pygame.quit()


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
