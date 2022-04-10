import os
from math import sqrt
from random import randint
from time import time
from typing import Any, Dict, Tuple

import pygame
from pygame.constants import (K_ESCAPE, KEYDOWN,  # §\label{srcBubble1101}§
                              KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, K_p)


class BubbleContainer:
    def __init__(self, filename: str) -> None:
        imagename = Game.get_image(filename)
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Game.radius["min"], Game.radius["max"] + 1)
        }

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Game.radius["min"], radius)
        radius = min(Game.radius["max"], radius)
        return self._images[radius]


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


class Background:
    def __init__(self) -> None:
        super().__init__()
        imagename = Game.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Game.window.size)
        self.rect = self.image.get_rect()


class Pause(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = Game.get_image("pause.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dirty = 1


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self, speed: int) -> None:
        super().__init__()
        self.mode = "blue"
        self.radius = Game.radius["min"]
        self.image = Game.bubble_container[self.mode].get(self.radius)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1
        self.fradius = float(self.radius)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Game.deltatime
                self.fradius = min(self.fradius, Game.radius["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = Game.bubble_container[self.mode].get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.dirty = 1
            elif kwargs["action"] == "sting":
                self.stung()
        elif "mode" in kwargs.keys():
            self.set_mode(kwargs["mode"])

    def set_mode(self, mode: str) -> None:
        if mode != self.mode:
            self.dirty = 1
            self.mode = mode
            self.image = Game.bubble_container[self.mode].get(self.radius)

    def randompos(self) -> None:
        bubbledistance = Game.distance + Game.radius["min"]
        centerx = randint(Game.playground.left + bubbledistance, Game.playground.right - bubbledistance)
        centery = randint(Game.playground.top + bubbledistance, Game.playground.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def stung(self):
        self.kill()
        Game.points += self.radius


class Points(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.oldpoints = -1
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.oldpoints != Game.points:
            self.image = self._font.render(f"Points: {Game.points}", True, "red")
            self.rect = self.image.get_rect()
            self.rect.left = Game.box.left
            self.rect.top = Game.box.top
            self.dirty = 1


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
    box = pygame.rect.Rect(90, 770, 1055, 1300)
    points = 0
    bubble_container: Dict[str, BubbleContainer] = {}

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
        Game.bubble_container["blue"] = BubbleContainer("blase1.png")
        Game.bubble_container["red"] = BubbleContainer("blase2.png")
        self._background = Background()
        self._timer_bubble = Timer(500, False)
        self._timer_bubble_speed = Timer(1000, False)
        self._bubble_speed = 10
        self._all_sprites = pygame.sprite.LayeredDirty()
        self._all_sprites.clear(self._screen, self._background.image)
        self._all_sprites.set_timing_treshold(1000.0/Game.fps)
        self._all_sprites.add(Points())
        self._running = True
        self._pausing = False                                   # §\label{srcBubble1102}§
        self._pause = Pause()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == KEYUP:
                if event.key == K_p:                            # §\label{srcBubble1103}§
                    self.setpause()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3:                           # right§\label{srcBubble1104}§
                    self.setpause()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:                           # left
                    self.sting(pygame.mouse.get_pos())

    def draw(self) -> None:
        rects = self._all_sprites.draw(self._screen)
        # pygame.draw.rect(self._screen, "red", Game.playground, 2)
        # for b in self._all_bubbles:
        #     pygame.draw.rect(self._screen, "red", b.rect, 2)  # type: ignore
        pygame.display.update(rects)  # type: ignore

    def update(self) -> None:
        if not self._pausing and self._running:                 # Pausenbildschirm§\label{srcBubble1107}§
            if self.check_bubblecollision():
                self._running = False
            else:
                self._all_sprites.update(action="grow")
                self.spawn_bubble()
            self.set_mousecursor()

    def setpause(self):
        if not self._pausing:
            self._all_sprites.add(self._pause)
        else:
            self._pause.kill()
        self._pausing = not self._pausing

    def spawn_bubble(self) -> None:
        if self._timer_bubble_speed.is_next_stop_reached():
            if self._bubble_speed < 100:
                self._bubble_speed += 5
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_sprites) <= Game.max_bubbles:
                b = Bubble(self._bubble_speed)
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
                        bubble1.update(mode="red")
                        bubble2.update(mode="red")
                        return True
                    if not Game.playground.contains(bubble1):
                        bubble1.update(mode="red")
                        return True
                    if not Game.playground.contains(bubble2):
                        bubble2.update(mode="red")
                        return True
        return False

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
        pygame.time.wait(2000)
        pygame.quit()


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
