import os
from random import choice, randint
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT


class MyEvents:                                 # Nur wegen Autovervollständigung§\label{srcEvent0100}§
    BUTTONPRESSED = pygame.USEREVENT + 0        # EventID für die Buttons§\label{srcEvent0101}§
    OVERFLOW = pygame.USEREVENT + 1             # EventID für den  Überlauf§\label{srcEvent0102}§


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (600, 150))
    FPS = 60
    DELTATIME = 1.0/FPS
    STARTNOFPARTICLES = 999
    NOFBOXES = 3
    BOXWIDTH = 50


class Button(pygame.sprite.Sprite):

    def __init__(self, text: str, position: Tuple[int], *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.font = pygame.font.SysFont(None, 30)
        self.centerxy = (Settings.WINDOW.centerx, self.font.get_height()//2)
        self._text = text
        self.image = self.font.render(self._text, True, "black")
        self.rect = self.image.get_rect(topleft=(position))

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "pressed":
                evt = pygame.event.Event(MyEvents.BUTTONPRESSED, text=self._text)  # §\label{srcEvent0103}§
                pygame.event.post(evt)                                             # §\label{srcEvent0104}§
        return super().update(*args, **kwargs)


class Particle(pygame.sprite.Sprite):

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.surface.Surface((randint(3, 6), randint(3, 6)))
        self.image.fill((0, randint(100, 255), 0))
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.topleft = (randint(30, Settings.WINDOW.right-30), randint(30, Settings.WINDOW.bottom-30), )
        self._speed = randint(100, 400)
        self._direction = pygame.Vector2(choice((-1, 1)), choice((-1, 1)))
        self._halted = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                if not self._halted:
                    self._move()
            elif kwargs["action"] == "Start":
                self._halted = False
            elif kwargs["action"] == "Stop":
                self._halted = True

    def _move(self) -> None:
        self.rect.move_ip(self._speed*self._direction*Settings.DELTATIME)
        if self.rect.left < 0:
            self._direction[0] *= -1
            self.rect.left = 0
        if self.rect.right > Settings.WINDOW.right:
            self._direction[0] *= -1
            self.rect.right = Settings.WINDOW.right
        if self.rect.top < 0:
            self._direction[1] *= -1
            self.rect.top = 0
        if self.rect.bottom > Settings.WINDOW.bottom:
            self._direction[1] *= -1
            self.rect.bottom = Settings.WINDOW.bottom


class Box(pygame.sprite.Sprite):

    def __init__(self, index: int, position: Tuple[int], *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.surface.Surface((Settings.BOXWIDTH, 20))
        self.rect = self.image.get_rect(center=position)
        self._font = pygame.font.SysFont(None, 30)
        self._counter = 0
        self._index = index
        self._fill()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "counter" in kwargs.keys():
            if kwargs["counter"] == "inc":
                self._counter += 1
                if self._counter == 10:                         # Überlauf §\label{srcEvent0105}§
                    evt = pygame.event.Event(MyEvents.OVERFLOW, index=self._index)
                    pygame.event.post(evt)
                    self._counter = 0
                self._fill()
        return super().update(*args, **kwargs)

    def _fill(self) -> None:
        self.image.fill("gray")
        number = self._font.render(f"{self._counter}", False, "Blue")
        self.image.blit(number, (18, 1))


class Game:

    def __init__(self) -> None:
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("Event (2)")
        self._all_sprites = pygame.sprite.Group()
        self._all_particles = pygame.sprite.Group()
        self._generate_particles(Settings.STARTNOFPARTICLES)
        self._all_buttons = pygame.sprite.Group()
        self._all_buttons.add(Button("Start", (30, Settings.WINDOW.bottom - 30), self._all_sprites))
        self._all_buttons.add(Button("Stop", (100, Settings.WINDOW.bottom - 30), self._all_sprites))
        self._all_boxes = pygame.sprite.Group()
        self._generate_boxes(Settings.NOFBOXES)
        self._running = True

    def run(self) -> None:
        time_previous = time()
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._check_button_pressed(event.pos)
            elif event.type == MyEvents.BUTTONPRESSED:          # §\label{srcEvent0106}§
                self._all_particles.update(action=event.text)
            elif event.type == MyEvents.OVERFLOW:               # §\label{srcEvent0107}§
                if event.index < Settings.NOFBOXES-1:
                    self._all_boxes.sprites()[event.index+1].update(counter="inc")

    def update(self):
        self._all_buttons.update()
        self._all_particles.update(action="move")
        self._check_boxcollision()

    def draw(self) -> None:
        self._screen.fill("white")
        self._all_sprites.draw(self._screen)
        pygame.display.update()

    def _generate_boxes(self, number: int) -> None:
        for i in range(number):
            self._all_boxes.add(Box(i, (Settings.WINDOW.right - 50 - i * 100, Settings.WINDOW.centery), self._all_sprites))

    def _generate_particles(self, number: int) -> None:
        for i in range(number):
            self._all_particles.add(Particle(self._all_sprites))

    def _check_button_pressed(self, position: Tuple[int]) -> None:
        for b in self._all_buttons.sprites():
            if b.rect.collidepoint(position):
                b.update(action="pressed")

    def _check_boxcollision(self) -> None:
        for p in self._all_particles.sprites():
            for b in self._all_boxes.sprites():
                if p.rect.colliderect(b):
                    self._all_boxes.sprites()[0].update(counter="inc")
                    p.kill()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
