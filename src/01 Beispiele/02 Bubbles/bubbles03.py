import os
from random import randint
from time import time
from typing import Any, Dict

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
    RADIUS = {"min": 15}
    DISTANCE = 50
    PLAYGROUND = pygame.rect.Rect(90, 90, 1055, 615)
    MAX_BUBBLES = PLAYGROUND.height * PLAYGROUND.width // 10000  # Erfahrungswert§\label{srcBubble0301}§


    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.PATH["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.PATH["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.PATH["sound"], filename)



class Timer:
    def __init__(self, duration: int, with_start: bool = True) -> None:
        self.duration = duration
        if with_start:
            self._next = pygame.time.get_ticks()
        else:
            self._next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        if pygame.time.get_ticks() > self._next:
            self._next = pygame.time.get_ticks() + self.duration
            return True
        return False


class Background(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = Settings.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Settings.WINDOW.size)
        self.rect = self.image.get_rect()
        self.dirty = 1


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self.radius = Settings.RADIUS["min"]
        imagename = Settings.get_image("blase1.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.RADIUS["min"], Settings.RADIUS["min"]))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def randompos(self) -> None:
        bubbledistance = Settings.DISTANCE + Settings.RADIUS["min"]
        centerx = randint(Settings.PLAYGROUND.left + bubbledistance, Settings.PLAYGROUND.right - bubbledistance)
        centery = randint(Settings.PLAYGROUND.top + bubbledistance, Settings.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption(Settings.CAPTION)
        self._clock = pygame.time.Clock()
        self._background = Background()
        self._timer_bubble = Timer(500, False)
        self._all_sprites = pygame.sprite.LayeredDirty()
        self._all_sprites.clear(self._screen, self._background.image)
        self._all_sprites.set_timing_treshold(1000.0/Settings.FPS)
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False

    def draw(self) -> None:
        rects = self._all_sprites.draw(self._screen)
        pygame.display.update(rects)

    def update(self) -> None:
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_sprites) <= Settings.MAX_BUBBLES:  # Platz?§\label{srcBubble0306}§
                b = Bubble()
                for _ in range(100):
                    b.randompos()
                    b.radius += Settings.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self._all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= Settings.DISTANCE
                    if not collided:
                        self._all_sprites.add(b)
                        break

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
