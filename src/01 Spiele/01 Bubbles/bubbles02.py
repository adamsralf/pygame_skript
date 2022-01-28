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
    radius = {"min": 15}                                        # Radius Startwert§\label{srcBubble0201}§
    distance = 50                                               # Rand-/Blasenabstand§\label{srcBubble0202}§
    playground = pygame.Rect(90, 90, 1055, 615)                 # Rechteck im Aquarium§\label{srcBubble0203}§

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


class Bubble(pygame.sprite.Sprite):
    def __init__(self, filename: str = "blase1.png") -> None:
        super().__init__()
        self.radius = Settings.radius["min"]
        self.image = pygame.image.load(os.path.join(Settings.path["image"], filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.radius["min"], Settings.radius["min"]))
        self.rect = self.image.get_rect()

    def update(self) -> None:
        pass

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
        self._background = pygame.sprite.GroupSingle(Background())  # Timer 500ms§\label{srcBubble0204}§
        self._timer_bubble = Timer(500, False)                  # Timer 500ms§\label{srcBubble0205}§
        self._all_bubbles = pygame.sprite.Group()               # Alle Blasen §\label{srcBubble0206}§
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
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            b = Bubble()
            tries = 100
            while tries > 0:
                b.randompos()
                b.radius += Settings.distance                   # Abstand zu Blasen§\label{srcBubble0207}§
                collided = pygame.sprite.spritecollide(b, self._all_bubbles, False, pygame.sprite.collide_circle)
                b.radius -= Settings.distance                   # Alter Radius!§\label{srcBubble0208}§
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
