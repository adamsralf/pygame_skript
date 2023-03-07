import os
from math import cos, pi, sin
from random import randint, random
from time import time
from typing import Any, Dict

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (400, 200))
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    FPS = 60
    DELTATIME = 1.0/FPS


class Ball(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.radius = randint(5, 25)
        fullfilename = os.path.join(Settings.PATH["image"], "blue2.png")
        self.image = pygame.image.load(fullfilename).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()
        self.speed = pygame.math.Vector2()
        self.selectimpuls()
        self.position = pygame.math.Vector2()
        self.selectposition()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.position += (self.speed * Settings.DELTATIME)
                self.position2rect()
            if self.rect.right >= Settings.WINDOW.right:
                self.rect.right = Settings.WINDOW.right - 1
                self.rect2position()
                self.speed.x *= -1
            elif self.rect.left <= Settings.WINDOW.left:
                self.rect.left = Settings.WINDOW.left + 1
                self.rect2position()
                self.speed.x *= -1
            if self.rect.top <= Settings.WINDOW.top:
                self.rect.top = Settings.WINDOW.top + 1
                self.rect2position()
                self.speed.y *= -1
            elif self.rect.bottom >= Settings.WINDOW.bottom:
                self.rect.bottom = Settings.WINDOW.bottom - 1
                self.rect2position()
                self.speed.y *= -1

    def position2rect(self):
        self.rect.centerx = round(self.position.x)
        self.rect.centery = round(self.position.y)

    def rect2position(self):
        self.position.x = self.rect.centerx
        self.position.y = self.rect.centery

    def selectposition(self):
        innerrect = Settings.WINDOW.inflate(-self.radius * 2.0, -self.radius * 2.0)
        self.position.x = randint(innerrect.left, innerrect.right)
        self.position.y = randint(innerrect.top, innerrect.bottom)
        self.position2rect()

    def selectimpuls(self):
        velocity = randint(50, 100)
        angle = random() * 2.0 * pi
        self.speed.x = velocity * sin(angle)
        self.speed.y = velocity * -cos(angle)


class Game:

    def __init__(self) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "20, 40"
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        self._background = pygame.surface.Surface(Settings.WINDOW.size)
        self._background.fill("grey")
        pygame.display.set_caption("Elastische Kreiskollision")
        self._all_balls = pygame.sprite.Group()
        self.add_ball()
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
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.add_ball()
                elif event.button == 3:
                    self.remove_ball()

    def update(self):
        self._all_balls.update(action="move")

    def draw(self) -> None:
        self._screen.blit(self._background, (0, 0))
        self._all_balls.draw(self._screen)
        pygame.display.update()

    def add_ball(self):
        ball = Ball()
        ball.radius += 5                                    # §\label{srcImpuls01a01}§
        tries = 10
        while tries > 0:
            tries -= 1
            if pygame.sprite.spritecollide(ball, self._all_balls, False, pygame.sprite.collide_circle):
                ball.selectposition()
            else:
                ball.radius -= 5                            # §\label{srcImpuls01a02}§
                self._all_balls.add(ball)
                return

    def remove_ball(self):
        if len(self._all_balls) > 0:
            self._all_balls.sprites()[0].kill()


def main():
    Game().run()


if __name__ == "__main__":
    main()
