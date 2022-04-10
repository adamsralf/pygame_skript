import os
import random
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Settings(object):
    window = {'width': 300, 'height': 300}
    fps = 60
    title = "Animation"
    deltatime = 1.0 / fps
    path: dict[str, str] = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")

    @staticmethod
    def dim() -> Tuple[int, int]:
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name: str) -> str:
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name: str) -> str:
        return os.path.join(Settings.path['image'], name)


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
                bitmap.set_colorkey(colorkey)           # Transparenz herstellen §\label{srcAnimation0101}§
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
        rocknb = random.randint(6, 9)                                    # Felsennummer §\label{srcAnimation0201}§
        self.image: pygame.surface.Surface = pygame.image.load(Settings.imagepath(f"felsen{rocknb}.png")).convert_alpha()
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.centerx = random.randint(self.rect.width, Settings.window['width']-self.rect.width)
        self.rect.centery = random.randint(self.rect.height, Settings.window['height']-self.rect.height)
        self.anim = Animation([f"explosion0{i}.png" for i in range(1, 5)], False, 50)  # §\label{srcAnimation0202}§
        self.timer_lifetime = Timer(random.randint(100, 2000), False)   # Lebenszeit §\label{srcAnimation0203}§
        self.bumm = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.timer_lifetime.is_next_stop_reached():
            self.bumm = True
        if self.bumm:
            self.image = self.anim.next()
            c = self.rect.center                                        # Zentrum §\label{srcAnimation0204}§
            self.rect = self.image.get_rect()
            self.rect.center = c
        if self.anim.is_ended():
            self.kill()


class ExplosionAnimation(object):

    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.all_rocks = pygame.sprite.Group()
        self.timer_newrock = Timer(500)                                  # Timer §\label{srcAnimation0205}§
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.fps)
            time_current = time()
            Settings.deltatime = time_current - time_previous
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
        if self.timer_newrock.is_next_stop_reached():                   # 500ms? §\label{srcAnimation0206}§
            self.all_rocks.add(Rock())
        self.all_rocks.update()

    def draw(self) -> None:
        self.screen.fill("black")
        self.all_rocks.draw(self.screen)
        pygame.display.flip()


def main():
    anim = ExplosionAnimation()
    anim.run()


if __name__ == '__main__':
    main()
