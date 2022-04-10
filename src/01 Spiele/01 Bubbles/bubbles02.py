import os
from random import randint
from time import time
from typing import Any, Dict

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


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self.radius = Game.radius["min"]
        imagename = Game.get_image("blase1.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Game.radius["min"], Game.radius["min"]))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

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
    radius = {"min": 15}                                        # Radius Startwert§\label{srcBubble0201}§
    distance = 50                                               # Rand-/Blasenabstand§\label{srcBubble0202}§
    playground = pygame.rect.Rect(90, 90, 1055, 615)            # Rechteck im Aquarium§\label{srcBubble0203}§

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
        self._background = Background()                                # §\label{srcBubble0204}§
        self._timer_bubble = Timer(500, False)                         # Timer 500ms§\label{srcBubble0205}§
        self._all_sprites = pygame.sprite.LayeredDirty()               # Alle Blasen §\label{srcBubble0206}§
        self._all_sprites.clear(self._screen, self._background.image)  # §\label{srcBubble0209}§
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
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self._timer_bubble.is_next_stop_reached():
            b = Bubble()
            tries = 100
            while tries > 0:
                b.randompos()
                b.radius += Game.distance                   # Abstand zu Blasen§\label{srcBubble0207}§
                collided = pygame.sprite.spritecollide(b, self._all_sprites, False, pygame.sprite.collide_circle)
                b.radius -= Game.distance                   # Alter Radius!§\label{srcBubble0208}§
                if collided:
                    tries -= 1
                else:
                    self._all_sprites.add(b)
                    break

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
