import os
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, K_KP_MINUS, K_KP_PLUS, KEYDOWN, QUIT


class Settings():
    window = {'width': 300, 'height': 200}
    fps = 60
    deltatime = 1.0 / fps
    title = "Animation"
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


class Cat(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.animation = Animation([f"cat{i}.bmp" for i in range(6)], True, 100, (0, 0, 0))  # §\label{srcAnimation0102}§
        self.image: pygame.surface.Surface = self.animation.next()
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "animation_delta" in kwargs.keys():
            self.change_animation_time(kwargs["animation_delta"])
        self.image = self.animation.next()
        # implement game logic here

    def change_animation_time(self, delta: int) -> None:
        self.animation.timer.change_duration(delta)


class CatAnimation():

    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.cat = pygame.sprite.GroupSingle(Cat())
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
                elif event.key == K_KP_PLUS:
                    self.cat.sprite.update(animation_delta=-10)
                elif event.key == K_KP_MINUS:
                    self.cat.sprite.update(animation_delta=10)

    def update(self) -> None:
        self.cat.update()

    def draw(self) -> None:
        self.screen.fill("gray")
        self.cat.draw(self.screen)
        text_image = self.font.render(f"animation time: {self.cat.sprite.animation.timer.duration}", True, "white")
        text_rect = text_image.get_rect()
        text_rect.centerx = Settings.window['width'] // 2
        text_rect.bottom = Settings.window['height'] - 50
        self.screen.blit(text_image, text_rect)
        pygame.display.flip()


def main():
    anim = CatAnimation()
    anim.run()


if __name__ == '__main__':
    main()
