import os
from math import sqrt
from random import randint
from time import time
from typing import Any, Dict, Tuple

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


class BubbleContainer:
    def __init__(self, filename: str) -> None:
        imagename = Settings.get_image(filename)
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(Settings.RADIUS["min"], Settings.RADIUS["max"] + 1)}

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(Settings.RADIUS["min"], radius)
        radius = min(Settings.RADIUS["max"], radius)
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


class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = Settings.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Settings.WINDOW.size)
        self.rect = self.image.get_rect()


class Message(pygame.sprite.Sprite):
    def __init__(self, filename: str) -> None:
        super().__init__()
        imagename = Settings.get_image(filename)
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.rect = self.image.get_rect()


class Bubble(pygame.sprite.Sprite):
    def __init__(self, speed: int) -> None:
        super().__init__()
        self.mode = "blue"
        self.radius = Settings.RADIUS["min"]
        self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.fradius = float(self.radius)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Settings.DELTATIME
                self.fradius = min(self.fradius, Settings.RADIUS["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
            elif kwargs["action"] == "sting":
                self.stung()
        elif "mode" in kwargs.keys():
            self.set_mode(kwargs["mode"])

    def set_mode(self, mode: str) -> None:
        if mode != self.mode:
            self.mode = mode
            self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)

    def randompos(self) -> None:
        bubbledistance = Settings.DISTANCE + Settings.RADIUS["min"]
        centerx = randint(Settings.PLAYGROUND.left + bubbledistance, Settings.PLAYGROUND.right - bubbledistance)
        centery = randint(Settings.PLAYGROUND.top + bubbledistance, Settings.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def stung(self):
        self.kill()
        Settings.POINTS += self.radius


class Points(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.oldpoints = -1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.oldpoints != Settings.POINTS:
            self.image = self._font.render(f"Points: {Settings.POINTS}", True, "red")
            self.rect = self.image.get_rect()
            self.rect.left = Settings.BOX.left
            self.rect.top = Settings.BOX.top


class Game:
    BUBBLE_CONTAINER: Dict[str, BubbleContainer] = {}
    SOUND_CONTAINER: Dict[str, pygame.mixer.Sound] = {}  # §\label{srcBubble1301}§

    def __init__(self) -> None:
        pygame.init()
        self._window = pygame.Window(size=Settings.WINDOW.size, title=Settings.CAPTION, position=pygame.WINDOWPOS_CENTERED)
        self._screen = self._window.get_surface()
        self._clock = pygame.time.Clock()
        Game.BUBBLE_CONTAINER["blue"] = BubbleContainer("blase1.png")
        Game.BUBBLE_CONTAINER["red"] = BubbleContainer("blase2.png")
        Game.SOUND_CONTAINER["bubble"] = pygame.mixer.Sound(Settings.get_sound("plopp1.mp3"))  # §\label{srcBubble1302}§
        Game.SOUND_CONTAINER["burst"] = pygame.mixer.Sound(Settings.get_sound("burst.mp3"))
        Game.SOUND_CONTAINER["clash"] = pygame.mixer.Sound(Settings.get_sound("glas.wav"))
        self._background = pygame.sprite.GroupSingle(Background())
        self._all_sprites = pygame.sprite.Group()
        self._running = True
        self._pausing = False
        self._pause = Message("pause.png")
        self._restart = Message("neustart.png")

        self.restart()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.setpause()
                elif event.key == pygame.K_j:
                    self._do_start = True
                elif event.key == pygame.K_n:
                    self._running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # right
                    self.setpause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left
                    self.sting(pygame.mouse.get_pos())

    def draw(self) -> None:
        self._background.draw(self._screen)
        self._all_sprites.draw(self._screen)
        self._window.flip()

    def update(self) -> None:
        if self._do_start:
            self.restart()
        if not self._pausing and self._running:
            if self.check_bubblecollision():
                if not self._restarting:
                    Game.SOUND_CONTAINER["clash"].play()  # §\label{srcBubble1305}§
                    self._all_sprites.add(self._restart)
                    self._restarting = True
            else:
                self._all_sprites.update(action="grow")
                self.spawn_bubble()
            self.set_mousecursor()

    def restart(self):
        Settings.POINTS = 0
        self._all_sprites.empty()
        self._all_sprites.add(Points())
        self._bubble_speed = 10
        self._timer_bubble = Timer(500, False)
        self._timer_bubble_speed = Timer(10000, False)
        self._do_start = False
        self._restarting = False

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
            if len(self._all_sprites) <= Settings.MAX_BUBBLES:
                b = Bubble(self._bubble_speed)
                for _ in range(100):
                    b.randompos()
                    b.radius += Settings.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self._all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= Settings.DISTANCE
                    if not collided:
                        self._all_sprites.add(b)
                        Game.SOUND_CONTAINER["bubble"].play()  # §\label{srcBubble1303}§
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        if hasattr(sprite, "radius"):
            deltax = point[0] - sprite.rect.centerx
            deltay = point[1] - sprite.rect.centery
            return sqrt(deltax * deltax + deltay * deltay) <= sprite.radius
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
                Game.SOUND_CONTAINER["burst"].play()  # §\label{srcBubble1304}§
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
                    if not Settings.PLAYGROUND.contains(bubble1):
                        bubble1.update(mode="red")
                        return True
                    if not Settings.PLAYGROUND.contains(bubble2):
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
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
