import os
import random
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Settings(object):
    WINDOW = pygame.rect.Rect((0, 0), (300, 300))
    FPS = 60
    TITLE = "Animation"
    DELTATIME = 1.0 / FPS
    PATH: dict[str, str] = {}
    PATH['file'] = os.path.dirname(os.path.abspath(__file__))
    PATH['image'] = os.path.join(PATH['file'], "images")

    @staticmethod
    def filepath(name: str) -> str:
        return os.path.join(Settings.PATH['file'], name)

    @staticmethod
    def imagepath(name: str) -> str:
        return os.path.join(Settings.PATH['image'], name)


class Timer():

    def __init__(self, duration: int, with_start: bool = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta: int = 10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0


class Animation():

    def __init__(self, namelist: list[str], endless: bool, animationtime: int, colorkey: tuple[int, int, int] | None = None) -> None:
        self.images: list[pygame.surface.Surface] = []
        self.endless = endless
        self.timer = Timer(animationtime)
        for filename in namelist:
            if colorkey == None:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
            else:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert()
                bitmap.set_colorkey(colorkey)
            self.images.append(bitmap)
        self.imageindex = -1

    def next(self) -> pygame.surface.Surface:
        if self.timer.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                if self.endless:
                    self.imageindex = 0
                else:
                    self.imageindex = len(self.images) - 1
        return self.images[self.imageindex]

    def is_ended(self) -> bool:
        if self.endless:
            return False
        return self.imageindex >= len(self.images) - 1


class Rock(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        rocknb = random.randint(6, 9)
        self.image = pygame.image.load(Settings.imagepath(f"felsen{rocknb}.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(self.rect.width, Settings.WINDOW.width-self.rect.width)
        self.rect.centery = random.randint(self.rect.height, Settings.WINDOW.height-self.rect.height)
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = pygame.math.Vector2(random.randint(-100, 100), random.randint(-100, 100))
        self.anim = Animation([f"explosion0{i}.png" for i in range(1, 5)], False, 50)
        self.bumm = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                if self.bumm:
                    self.image = self.anim.next()
                    c = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = c
                else:
                    newpos = self.position + self.speed * Settings.DELTATIME
                    self.rect.left = newpos.x
                    self.rect.top = newpos.y
                    if self.rect.top <= 0 or self.rect.bottom >= Settings.WINDOW.height:
                        self.speed.y *= -1
                    if self.rect.left <= 0 or self.rect.right >= Settings.WINDOW.width:
                        self.speed.x *= -1
                    self.position += self.speed * Settings.DELTATIME
            elif kwargs["action"] == "bumm":
                self.bumm = True
        if self.anim.is_ended():
            self.kill()


class ExplosionAnimation(object):

    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption(Settings.TITLE)
        self.clock = pygame.time.Clock()
        self.all_rocks = pygame.sprite.Group()
        self.timer_newrock = Timer(500)
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        if self.timer_newrock.is_next_stop_reached():
            self.all_rocks.add(Rock())
        self.all_rocks.update(action="move")
        for a in self.all_rocks.sprites():
            for b in self.all_rocks.sprites():
                if a != b:
                    if pygame.sprite.collide_rect(a, b):
                        a.update(action="bumm")
                        b.update(action="bumm")

    def draw(self) -> None:
        self.screen.fill("black")
        self.all_rocks.draw(self.screen)
        pygame.display.flip()


def main():
    anim = ExplosionAnimation()
    anim.run()


if __name__ == '__main__':
    main()
