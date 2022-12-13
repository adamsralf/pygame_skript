import os
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, K_KP_MINUS, K_KP_PLUS, KEYDOWN, QUIT


class Settings():
    WINDOW = pygame.rect.Rect((0, 0), (300, 200))
    FPS = 60
    DELTATIME = 1.0 / FPS
    TITLE = "Animation"
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


class Cat(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.images: list[pygame.surface.Surface] = []
        for i in range(6):                                  # Animations-Sprites laden §\label{srcAnimation0001}§
            bitmap = pygame.image.load(Settings.imagepath(f"cat{i}.bmp")).convert()
            bitmap.set_colorkey("black")
            self.images.append(bitmap)
        self.imageindex = 0
        self.image: pygame.surface.Surface = self.images[self.imageindex]
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = Settings.WINDOW.center
        self.animation_time = Timer(100)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "animation_delta" in kwargs.keys():
            self.change_animation_time(kwargs["animation_delta"])
        if self.animation_time.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            self.image = self.images[self.imageindex]
            # implement game logic here

    def change_animation_time(self, delta: int) -> None:
        self.animation_time.change_duration(delta)


class CatAnimation():

    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption(Settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.cat = pygame.sprite.GroupSingle(Cat())         # Meine Katze §\label{srcAnimation0002}§
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
                elif event.key == K_KP_PLUS:
                    self.cat.sprite.update(animation_delta=-10)
                elif event.key == K_KP_MINUS:
                    self.cat.sprite.update(animation_delta=10)

    def update(self) -> None:
        self.cat.update()

    def draw(self) -> None:
        self.screen.fill("gray")
        self.cat.draw(self.screen)
        text_image = self.font.render(f"animation time: {self.cat.sprite.animation_time.duration}", True, "white")
        text_rect = text_image.get_rect()
        text_rect.centerx = Settings.WINDOW.centerx
        text_rect.bottom = Settings.WINDOW.bottom - 50
        self.screen.blit(text_image, text_rect)
        pygame.display.flip()


def main():
    anim = CatAnimation()
    anim.run()


if __name__ == '__main__':
    main()
