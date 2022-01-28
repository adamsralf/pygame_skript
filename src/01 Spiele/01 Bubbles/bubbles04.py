import os
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
    radius = {"min": 15, "max": 240}                            # Obergrenze§\label{srcBubble0400}§
    distance = 50
    playground = pygame.Rect(90, 90, 1055, 615)
    max_bubbles = playground.height * playground.width // 10000

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
        image = pygame.image.load(os.path.join(Settings.path["image"], "blase1.png")).convert_alpha()
        self._images = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Settings.radius["min"], Settings.radius["max"] + 1)
        }                                                       # §\label{srcBubble0403}§

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Settings.radius["min"], radius)            # Untere Grenze§\label{srcBubble0404}§
        radius = min(Settings.radius["max"], radius)            # Obere Grenze§\label{srcBubble0405}§
        return self._images[radius]


class Bubble(pygame.sprite.Sprite):
    def __init__(self, bubble_container: BubbleContainer, filename: str = "blase1.png") -> None:
        super().__init__()
        self._bubble_container = bubble_container               # Verweis auf Container§\label{srcBubble0406}§
        self.radius = Settings.radius["min"]
        self.image = self._bubble_container.get(self.radius)    # Zugriff auf Bubbles §\label{srcBubble0407}§
        self.rect = self.image.get_rect()

    def update(self) -> None:
        self.radius = min(self.radius + 1, Settings.radius["max"])  # Neuer Radius  §\label{srcBubble0410}§
        center = self.rect.center                               # Alter Kreismittelpunkt §\label{srcBubble0411}§
        self.image = self._bubble_container.get(self.radius)    # Neues größeres Image §\label{srcBubble0412}§
        self.rect = self.image.get_rect()
        self.rect.center = center                               # Neuer MP = Alter MP §\label{srcBubble0413}§

    def randompos(self) -> None:
        bubbledistance = Settings.distance + Settings.radius["min"]
        centerx = randint(Settings.playground.left + bubbledistance, Settings.playground.right - bubbledistance)
        centery = randint(Settings.playground.top + bubbledistance, Settings.playground.bottom - bubbledistance)
        self.rect.center = (centerx, centery)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.caption)
        self._clock = pygame.time.Clock()
        self._bubble_container = BubbleContainer()
        self._background = pygame.sprite.GroupSingle(Background())
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

    def draw(self) -> None:
        self._background.draw(self._screen)
        self._all_bubbles.draw(self._screen)
        pygame.display.flip()

    def update(self) -> None:
        self._all_bubbles.update()                              # Bubbles aktualisieren §\label{srcBubble0414}§
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_bubbles) <= Settings.max_bubbles:
                b = Bubble(self._bubble_container)              # Verweis auf Bubbles §\label{srcBubble0415}§
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
