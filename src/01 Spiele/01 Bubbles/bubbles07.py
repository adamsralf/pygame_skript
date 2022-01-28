import os
from math import sqrt
from random import randint
from typing import Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Settings:
    window = {"width": 1220, "height": 1002}
    fps = 60
    path = {}
    path["file"] = os.path.dirname(os.path.abspath(__file__))
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")
    caption = 'Fingerübung "Bubbles"'
    radius = {"min": 15, "max": 240}
    distance = 50
    playground = pygame.Rect(90, 90, 1055, 615)
    max_bubbles = playground.height * playground.width // 10000
    box = pygame.Rect(90, 770, 1055, 1300)                      # Ausgabebox§\label{srcBubble0700}§
    points = 0                                                  # Globaler Punktestand§\label{srcBubble0701}§

    @staticmethod
    def get_dim() -> Tuple[int, int]:
        return (Settings.window["width"], Settings.window["height"])


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


class Background(pygame.sprite.Sprite):
    def __init__(self, filename: str = "aquarium.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path["image"], filename)).convert()
        self.image = pygame.transform.scale(self.image, Settings.get_dim())
        self.rect = self.image.get_rect()


class BubbleContainer:
    def __init__(self) -> None:
        image = pygame.image.load(os.path.join(Settings.path["image"], "blue2.png")).convert_alpha()
        self._images = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Settings.radius["min"], Settings.radius["max"] + 1)
        }

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Settings.radius["min"], radius)
        radius = min(Settings.radius["max"], radius)
        return self._images[radius]


class Bubble(pygame.sprite.Sprite):
    def __init__(self, bubble_container: BubbleContainer, filename: str = "blue2.png") -> None:
        super().__init__()
        self._bubble_container = bubble_container
        self.radius = Settings.radius["min"]
        self.image = self._bubble_container.get(self.radius)
        self.rect = self.image.get_rect()

    def update(self) -> None:
        self.radius = min(self.radius + 1, Settings.radius["max"])
        center = self.rect.center
        self.image = self._bubble_container.get(self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def randompos(self) -> None:
        bubbledistance = Settings.distance + Settings.radius["min"]
        centerx = randint(Settings.playground.left + bubbledistance, Settings.playground.right - bubbledistance)
        centery = randint(Settings.playground.top + bubbledistance, Settings.playground.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        deltax = point[0] - self.rect.centerx
        deltay = point[1] - self.rect.centery
        return sqrt(deltax * deltax + deltay * deltay) <= self.radius

    def stung(self):
        self.kill()
        Settings.points += self.radius                          # Increment points§\label{srcBubble0702}§


class Points(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)

    def update(self) -> None:
        self.image = self._font.render(f"Points: {Settings.points}", True, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.left = Settings.box.left
        self.rect.top = Settings.box.top


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.caption)
        self._clock = pygame.time.Clock()
        self._bubble_container = BubbleContainer()
        self._background = pygame.sprite.GroupSingle(Background())
        self._points = pygame.sprite.GroupSingle(Points())      # Points§\label{srcBubble0703}§
        self._timer_bubble = Timer(500, False)
        self._all_bubbles = pygame.sprite.Group()
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:                           # left
                    self.sting(pygame.mouse.get_pos())

    def draw(self) -> None:
        self._background.draw(self._screen)
        self._all_bubbles.draw(self._screen)
        self._points.draw(self._screen)                         # Punkte ausgaben§\label{srcBubble0706}§
        pygame.display.flip()

    def update(self) -> None:
        self._all_bubbles.update()
        self._points.update()                                   # Punkte aktualisieren§\label{srcBubble0705}§
        self.spawn_bubble()
        self.set_mousecursor()

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_bubbles) <= Settings.max_bubbles:
                b = Bubble(self._bubble_container)
                tries = 100
                while tries > 0:
                    b.randompos()
                    b.radius += Settings.distance
                    collided = pygame.sprite.spritecollide(b, self._all_bubbles, False, pygame.sprite.collide_circle)
                    b.radius -= Settings.distance
                    if collided:
                        tries -= 1
                    else:
                        self._all_bubbles.add(b)
                        break

    def set_mousecursor(self) -> None:
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self._all_bubbles:
            if b.collidepoint(pos):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def sting(self, mousepos) -> None:
        for bubble in self._all_bubbles:
            if bubble.collidepoint(mousepos):
                bubble.stung()                                  # Nach Bubble verschoben§\label{srcBubble0704}§

    def run(self) -> None:
        self._running = True
        while self._running:
            self._clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()
