import os
from random import randint
from time import time
from typing import Any, Dict

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1220, 1002)
    FPS = 60
    DELTATIME = 1.0 / FPS
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")
    CAPTION = 'Fingerübung "Bubbles"'
    RADIUS = {"min": 15, "max": 240}  # Obergrenze§\label{srcBubble0400}§
    DISTANCE = 50
    PLAYGROUND = pygame.rect.Rect(90, 90, 1055, 615)
    MAX_BUBBLES = PLAYGROUND.height * PLAYGROUND.width // 10000

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


class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = Settings.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Settings.WINDOW.size)
        self.rect = self.image.get_rect()


class BubbleContainer:
    def __init__(self) -> None:
        imagename = Settings.get_image("blase1.png")
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(Settings.RADIUS["min"], Settings.RADIUS["max"] + 1)}  # §\label{srcBubble0403}§

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Settings.RADIUS["min"], radius)  # Untere Grenze§\label{srcBubble0404}§
        radius = min(Settings.RADIUS["max"], radius)  # Obere Grenze§\label{srcBubble0405}§
        return self._images[radius]


class Bubble(pygame.sprite.Sprite):
    def __init__(self, bubble_container: BubbleContainer) -> None:
        super().__init__()
        self._bubble_container = bubble_container  # Verweis auf Container§\label{srcBubble0406}§
        self.radius = Settings.RADIUS["min"]
        self.image = self._bubble_container.get(self.radius)  # Zugriff auf Bubbles §\label{srcBubble0407}§
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.fradius = float(self.radius)
        self.speed = 100

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Settings.DELTATIME
                self.fradius = min(self.fradius, Settings.RADIUS["max"])  # Neuer Radius  §\label{srcBubble0410}§
                self.radius = round(self.fradius)
                center = self.rect.center  # Alter Mittelpunkt §\label{srcBubble0411}§
                self.image = self._bubble_container.get(self.radius)  # Neues Image §\label{srcBubble0412}§
                self.rect = self.image.get_rect()
                self.rect.center = center  # Neuer MP = Alter MP §\label{srcBubble0413}§

    def randompos(self) -> None:
        bubbledistance = Settings.DISTANCE + Settings.RADIUS["min"]
        centerx = randint(Settings.PLAYGROUND.left + bubbledistance, Settings.PLAYGROUND.right - bubbledistance)
        centery = randint(Settings.PLAYGROUND.top + bubbledistance, Settings.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._window = pygame.Window(size=Settings.WINDOW.size, title=Settings.CAPTION, position=pygame.WINDOWPOS_CENTERED)
        self._screen = self._window.get_surface()
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
        self._bubble_container = BubbleContainer()
        self._timer_bubble = Timer(500, False)
        self._all_sprites = pygame.sprite.Group()
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False

    def draw(self) -> None:
        self._background.draw(self._screen)
        self._all_sprites.draw(self._screen)
        self._window.flip()

    def update(self) -> None:
        self._all_sprites.update(action="grow")  # Bubbles aktualisieren §\label{srcBubble0414}§
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_sprites) <= Settings.MAX_BUBBLES:
                b = Bubble(self._bubble_container)  # Verweis auf Bubbles §\label{srcBubble0415}§
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
    Game().run()


if __name__ == "__main__":
    main()
