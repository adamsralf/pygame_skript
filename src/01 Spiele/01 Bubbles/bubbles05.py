import os
from math import sqrt
from random import randint
from time import time
from typing import Any, Dict, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


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
        imagename = Game.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Game.window.size)
        self.rect = self.image.get_rect()
        self.dirty = 1


class BubbleContainer:
    def __init__(self) -> None:
        imagename = Game.get_image("blase1.png")
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Game.radius["min"], Game.radius["max"] + 1)
        }

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Game.radius["min"], radius)
        radius = min(Game.radius["max"], radius)
        return self._images[radius]


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self, bubble_container: BubbleContainer) -> None:
        super().__init__()
        self._bubble_container = bubble_container
        self.radius = Game.radius["min"]
        self.image = self._bubble_container.get(self.radius)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1
        self.fradius = float(self.radius)
        self.speed = 100

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Game.deltatime
                self.fradius = min(self.fradius, Game.radius["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = self._bubble_container.get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.dirty = 1

    def randompos(self) -> None:
        bubbledistance = Game.distance + Game.radius["min"]
        centerx = randint(Game.playground.left + bubbledistance, Game.playground.right - bubbledistance)
        centery = randint(Game.playground.top + bubbledistance, Game.playground.bottom - bubbledistance)
        self.rect.center = (centerx, centery)


class Game:
    window = pygame.rect.Rect(0, 0, 1220, 1002)
    fps = 60
    deltatime = 1.0/fps
    path: Dict[str, str] = {}
    path["file"] = os.path.dirname(os.path.abspath(__file__))
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")
    caption = 'Fingerübung "Bubbles"'
    radius = {"min": 15, "max": 240}
    distance = 50
    playground = pygame.rect.Rect(90, 90, 1055, 615)
    max_bubbles = playground.height * playground.width // 10000

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
        self._bubble_container = BubbleContainer()
        self._background = Background()
        self._timer_bubble = Timer(500, False)
        self._all_sprites = pygame.sprite.LayeredDirty()
        self._all_sprites.clear(self._screen, self._background.image)
        self._all_sprites.set_timing_treshold(1000.0/Game.fps)
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
        pygame.display.update(rects)  # type: ignore

    def update(self) -> None:
        self._all_sprites.update(action="grow")
        self.spawn_bubble()
        self.set_mousecursor()                                  # Mauscursor §\label{srcBubble0501}§

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_sprites) <= Game.max_bubbles:
                b = Bubble(self._bubble_container)
                tries = 100
                while tries > 0:
                    b.randompos()
                    b.radius += Game.distance
                    collided = pygame.sprite.spritecollide(b, self._all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= Game.distance
                    if collided:
                        tries -= 1
                    else:
                        self._all_sprites.add(b)
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        if hasattr(sprite, 'radius'):
            deltax = point[0] - sprite.rect.centerx  # type: ignore
            deltay = point[1] - sprite.rect.centery  # type: ignore
            return (sqrt(deltax * deltax + deltay * deltay) <= sprite.radius)  # type: ignore
        return False

    def set_mousecursor(self) -> None:
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self._all_sprites:
            if self.collidepoint(pos, b):                             # Innerhalb? §\label{srcBubble0502}§
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

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
