import os
from math import sqrt
from pdb import Restart
from random import randint
from typing import Tuple

import pygame
from pygame.constants import (K_ESCAPE, KEYDOWN,  # §\label{srcBubble1201}§
                              KEYUP, QUIT, K_j, K_n, K_p)


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
    box = pygame.Rect(90, 770, 1055, 1300)
    points = 0
    bubble_container = {}

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


class Foreground:
    def __init__(self, message: str) -> None:                   # Nachrichtentext§\label{srcBubble1202}§
        super().__init__()
        self._image = pygame.image.load(os.path.join(Settings.path["image"], "hintergrund.png")).convert_alpha()
        self._image = pygame.transform.scale(self._image, Settings.get_dim())
        self._image.set_alpha(150)
        self._rect_image = self._image.get_rect()
        font_bigsize = pygame.font.Font(pygame.font.get_default_font(), 40)
        self._text = font_bigsize.render(message, True, (255, 0, 0))  # rendern§\label{srcBubble1203}§
        self._rect_text = self._text.get_rect()
        self._rect_text.centerx = Settings.window["width"] // 2
        self._rect_text.centery = Settings.window["height"] // 2 - 50

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self._image, self._rect_image)
        screen.blit(self._text, self._rect_text)


class BubbleContainer:
    def __init__(self, filename: str) -> None:
        image = pygame.image.load(os.path.join(Settings.path["image"], filename)).convert_alpha()
        self._images = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Settings.radius["min"], Settings.radius["max"] + 1)
        }

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Settings.radius["min"], radius)
        radius = min(Settings.radius["max"], radius)
        return self._images[radius]


class Bubble(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.mode = "blue"
        self.radius = Settings.radius["min"]
        self.image = Settings.bubble_container[self.mode].get(self.radius)
        self.rect = self.image.get_rect()
        self._timer_growth = Timer(100, False)

    def update(self) -> None:
        if self._timer_growth.is_next_stop_reached():
            self.radius = min(self.radius + 1, Settings.radius["max"])
            center = self.rect.center
            self.image = Settings.bubble_container[self.mode].get(self.radius)
            self.rect = self.image.get_rect()
            self.rect.center = center

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        self.image = Settings.bubble_container[self.mode].get(self.radius)

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
        Settings.points += self.radius


class Points(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)

    def update(self) -> None:
        self.image = self._font.render(f"Points: {Settings.points}", True, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = Settings.box.topleft


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.caption)
        self._clock = pygame.time.Clock()
        Settings.bubble_container["blue"] = BubbleContainer("blase1.png")
        Settings.bubble_container["red"] = BubbleContainer("blase2.png")
        self._background = pygame.sprite.GroupSingle(Background())
        self._points = pygame.sprite.GroupSingle(Points())
        self._timer_bubble = Timer(1000, False)
        self._timer_bubble_duration = Timer(10000, False)
        self._all_bubbles = pygame.sprite.Group()
        self._running = True
        self._pause = Foreground("PAUSE")
        self._pausing = False
        self._restart = Foreground("Neustart (J/N)?")
        self._restarting = False
        self._do_start = False

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == KEYUP:
                if event.key == K_p:
                    self._pausing = not self._pausing
                elif event.key == K_j:                          # §\label{srcBubble1205}§
                    self._do_start = True
                elif event.key == K_n:                          # §\label{srcBubble1206}§
                    self._running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.sting(pygame.mouse.get_pos())
                elif event.button == 3:
                    self._pausing = not self._pausing

    def draw(self) -> None:
        self._background.draw(self._screen)
        self._all_bubbles.draw(self._screen)
        self._points.draw(self._screen)
        # pygame.draw.rect(self._screen, (255, 0, 0), Settings.playground, 2)
        # for b in self._all_bubbles:
        #     pygame.draw.rect(self._screen, (255, 0, 0), b.rect, 2)
        if self._pausing:
            self._pause.draw(self._screen)
        elif self._restarting:                                  # Abfragebildschirm?§\label{srcBubble1207}§
            self._restart.draw(self._screen)

        pygame.display.flip()

        pygame.display.flip()

    def update(self) -> None:
        if self._do_start:                                      # Neustart?§\label{srcBubble1208}§
            Settings.points = 0
            self._all_bubbles.empty()
            self._timer_bubble = Timer(1000, False)
            self._timer_bubble_duration = Timer(10000, False)
            self._do_start = False
            self._restarting = False
        if not self._pausing and self._running:
            if self.check_bubblecollision():
                self._restarting = True
            else:
                self._all_bubbles.update()
                self._points.update()
                self.spawn_bubble()
            self.set_mousecursor()

    def spawn_bubble(self) -> None:
        if self._timer_bubble_duration.is_next_stop_reached():
            self._timer_bubble.duration = max(self._timer_bubble.duration - 100, 400)
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_bubbles) <= Settings.max_bubbles:
                b = Bubble()
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
                bubble.stung()

    def check_bubblecollision(self) -> bool:
        for index1 in range(0, len(self._all_bubbles) - 1):
            for index2 in range(index1 + 1, len(self._all_bubbles)):
                bubble1 = self._all_bubbles.sprites()[index1]
                bubble2 = self._all_bubbles.sprites()[index2]
                if pygame.sprite.collide_circle(bubble1, bubble2):
                    bubble1.set_mode("red")
                    bubble2.set_mode("red")
                    return True
                if not Settings.playground.contains(bubble1):
                    bubble1.set_mode("red")
                    return True
                if not Settings.playground.contains(bubble2):
                    bubble2.set_mode("red")
                    return True
        return False

    def run(self) -> None:
        self._running = True
        while self._running:
            self._clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        # pygame.time.wait(2000)                                # §\label{srcBubble1209}§
        pygame.quit()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()
