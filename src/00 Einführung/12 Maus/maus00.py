import os
from time import time
from typing import Any, Dict, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT


class Ball(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        fullfilename = os.path.join(Game.PATH["image"], "blue2.png")
        self.image_orig = pygame.image.load(fullfilename).convert_alpha()
        self._scale = 10
        self.image = pygame.transform.scale(self.image_orig, (self._scale, self._scale))
        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "go" in kwargs.keys():                               # Parameter vorhanden?§\label{srcMaus0009}§
            if kwargs["go"]:
                self.rect.left = max(self.rect.left, Game.INNER_RECT.left)
                self.rect.right = min(self.rect.right, Game.INNER_RECT.right)
                self.rect.top = max(self.rect.top, Game.INNER_RECT.top)
                self.rect.bottom = min(self.rect.bottom, Game.INNER_RECT.bottom)
                c = self.rect.center                            # altes Zentrum merken
                self.image = pygame.transform.scale(self.image_orig, (self._scale, self._scale))
                self.rect = self.image.get_rect()
                self.rect.center = c                            # Zentrum zurücksetzen

        if "rotate" in kwargs.keys():                           # §\label{srcMaus0010}§
            self.rotate(kwargs["rotate"])

        if "scale" in kwargs.keys():                            # §\label{srcMaus0011}§
            self.resize(kwargs["scale"])

        if "center" in kwargs.keys():                           # §\label{srcMaus0012}§
            self.set_center(kwargs["center"])

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)

    def rotate(self, angle: float) -> None:
        self.image_orig = pygame.transform.rotate(self.image_orig, angle)

    def resize(self, delta: int) -> None:
        if self.rect.width < Game.INNER_RECT.width:
            if self._scale + delta > 0:
                self._scale += delta

    def set_center(self, center: Tuple[int, int]) -> None:
        self.rect.center = center


class Game:
    WINDOW = pygame.rect.Rect((0, 0), (600, 600))
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    INNER_RECT = pygame.rect.Rect(100, 100, WINDOW.width - 200, WINDOW.height - 200)
    DELTATIME = 60
    deltatime = 1.0/DELTATIME

    def __init__(self) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "650, 70"
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(Game.WINDOW.size)
        pygame.display.set_caption("Mausaktionen")
        self._ball = Ball()                                     # Ball-Objekt§\label{srcMaus0001}§
        self._running = True

    def run(self) -> None:
        time_previous = time()
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Game.DELTATIME)
            time_current = time()
            Game.deltatime = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == MOUSEBUTTONDOWN:                 # Maustaste gedrückt§\label{srcMaus0002}§
                if event.button == 1:                           # left§\label{srcMaus0004}§
                    self._ball.update(rotate=90)
                elif event.button == 2:                         # middle§\label{srcMaus0005}§
                    self._running = False
                elif event.button == 3:                         # right§\label{srcMaus0006}§
                    self._ball.update(rotate=-90)
                elif event.button == 4:                         # scroll up§\label{srcMaus0007}§
                    self._ball.update(scale=2)
                elif event.button == 5:                         # scroll down§\label{srcMaus0008}§
                    self._ball.update(scale=-2)

    def update(self):
        self._ball.update(center=pygame.mouse.get_pos())
        pygame.mouse.set_visible(
            not Game.INNER_RECT.collidepoint(pygame.mouse.get_pos())
        )                                                       # Unsichtbar?§\label{srcMaus0003}§
        self._ball.update(go=True)

    def draw(self) -> None:
        self._screen.fill((250, 250, 250))
        pygame.draw.rect(self._screen, "red", Game.INNER_RECT, 1)
        self._ball.draw(self._screen)
        pygame.display.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
