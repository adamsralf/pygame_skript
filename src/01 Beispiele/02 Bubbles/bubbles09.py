import os
from math import sqrt
from random import randint
from time import time
from typing import Any, Dict, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1220, 1002)
    FPS = 60
    DELTATIME = 1.0 / FPS
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")
    CAPTION = 'Fingerübung "Bubbles"'
    RADIUS = {"min": 15, "max": 240}
    DISTANCE = 50
    PLAYGROUND = pygame.rect.Rect(90, 90, 1055, 615)
    MAX_BUBBLES = PLAYGROUND.height * PLAYGROUND.width // 10000
    BOX = pygame.rect.Rect(90, 770, 1055, 1300)
    POINTS = 0

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


class BubbleContainer:
    def __init__(self) -> None:
        imagename = Settings.get_image("blase1.png")
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(Settings.RADIUS["min"], Settings.RADIUS["max"] + 1)}

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Settings.RADIUS["min"], radius)
        radius = min(Settings.RADIUS["max"], radius)
        return self._images[radius]


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self, bubble_container: BubbleContainer, speed: int) -> None:
        super().__init__()
        self._bubble_container = bubble_container
        self.radius = Settings.RADIUS["min"]
        self.image = self._bubble_container.get(self.radius)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1
        self.fradius = float(self.radius)
        self.speed = speed  # Wachstumsgeschwindigkeit§\label{srcBubble0900}§

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Settings.DELTATIME
                self.fradius = min(self.fradius, Settings.RADIUS["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = self._bubble_container.get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.dirty = 1
            elif kwargs["action"] == "sting":
                self.stung()

    def randompos(self) -> None:
        bubbledistance = Settings.DISTANCE + Settings.RADIUS["min"]
        centerx = randint(Settings.PLAYGROUND.left + bubbledistance, Settings.PLAYGROUND.right - bubbledistance)
        centery = randint(Settings.PLAYGROUND.top + bubbledistance, Settings.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def stung(self):
        self.kill()
        Settings.POINTS += self.radius


class Points(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.oldpoints = -1
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.oldpoints != Settings.POINTS:
            self.image = self._font.render(f"Points: {Settings.POINTS}", True, "red")
            self.rect = self.image.get_rect()
            self.rect.left = Settings.BOX.left
            self.rect.top = Settings.BOX.top
            self.dirty = 1


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption(Settings.CAPTION)
        self._clock = pygame.time.Clock()
        self._bubble_container = BubbleContainer()
        self._background = Background()
        self._timer_bubble = Timer(500, False)
        self._timer_bubble_speed = Timer(1000, False)  # §\label{srcBubble0901}§
        self._bubble_speed = 10
        self._all_sprites = pygame.sprite.LayeredDirty()
        self._all_sprites.clear(self._screen, self._background.image)
        self._all_sprites.set_timing_treshold(1000.0 / Settings.FPS)
        self._all_sprites.add(Points())
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # left
                    self.sting(pygame.mouse.get_pos())

    def draw(self) -> None:
        rects = self._all_sprites.draw(self._screen)
        # pygame.draw.rect(self._screen, "red", Settings.playground, 2)
        # for b in self._all_bubbles:
        #     pygame.draw.rect(self._screen, "red", b.rect, 2)  # type: ignore
        pygame.display.update(rects)  # type: ignore

    def update(self) -> None:
        if self.check_bubblecollision():
            self._running = False
        else:
            self._all_sprites.update(action="grow")
            self.spawn_bubble()
        self.set_mousecursor()

    def spawn_bubble(self) -> None:
        if self._timer_bubble_speed.is_next_stop_reached():  # §\label{srcBubble0902}§
            if self._bubble_speed < 100:
                self._bubble_speed += 5
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_sprites) <= Settings.MAX_BUBBLES:
                b = Bubble(self._bubble_container, self._bubble_speed)
                for _ in range(100):
                    b.randompos()
                    b.radius += Settings.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self._all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= Settings.DISTANCE
                    if not collided:
                        self._all_sprites.add(b)
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        if hasattr(sprite, "radius"):
            deltax = point[0] - sprite.rect.centerx  # type: ignore
            deltay = point[1] - sprite.rect.centery  # type: ignore
            return sqrt(deltax * deltax + deltay * deltay) <= sprite.radius  # type: ignore
        return False

    def set_mousecursor(self) -> None:
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self._all_sprites:
            if self.collidepoint(pos, b):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def sting(self, mousepos: Tuple[int, int]) -> None:
        for bubble in self._all_sprites:
            if self.collidepoint(mousepos, bubble):
                bubble.update(action="sting")

    def check_bubblecollision(self) -> bool:
        for index1 in range(0, len(self._all_sprites) - 1):
            for index2 in range(index1 + 1, len(self._all_sprites)):
                bubble1 = self._all_sprites.sprites()[index1]
                bubble2 = self._all_sprites.sprites()[index2]
                if type(bubble1).__name__ == "Bubble" and type(bubble2).__name__ == "Bubble":
                    if pygame.sprite.collide_circle(bubble1, bubble2):
                        return True
                    if not Settings.PLAYGROUND.contains(bubble1):
                        return True
                    if not Settings.PLAYGROUND.contains(bubble2):
                        return True
        return False

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
