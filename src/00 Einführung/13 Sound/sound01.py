import os
from time import time
from typing import Any

import pygame
from pygame.constants import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, KEYDOWN, QUIT


class Settings:
    WINDOW: pygame.rect.Rect = pygame.rect.Rect(0, 0, 800, 160)
    FPS = 60
    DELTATIME = 1.0 / FPS
    PATH: dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.PATH["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.PATH["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.PATH["sound"], filename)


class Ground(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        fullfilename = Settings.get_image("tankbrigade_part64.png")
        tile = pygame.image.load(fullfilename).convert()
        rect = tile.get_rect()
        self.image = pygame.Surface(Settings.WINDOW.size)
        for row in range(Settings.WINDOW.width // rect.width):
            for col in range(Settings.WINDOW.height // rect.height):
                self.image.blit(tile, (row * rect.width, col * rect.height))
        self.rect = self.image.get_rect()


class Tank(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self._image_filename = (209, 190, 202, 214, 226, 238, 250, 262)
        self._images: dict[str, list[pygame.surface.Surface]] = {"up": [], "down": [], "left": [], "right": []}
        for number in self._image_filename:
            fullfilename = Settings.get_image(f"tankbrigade_part{number}.png")
            picture = pygame.image.load(fullfilename).convert()
            picture.set_colorkey("black")
            self._images["up"].append(picture)
            self._images["down"].append(pygame.transform.rotate(picture, 180))
            self._images["left"].append(pygame.transform.rotate(picture, +90))
            self._images["right"].append(pygame.transform.rotate(picture, -90))
        self._direction = "right"
        self._imageindex = 0
        self.image = self._images[self._direction][self._imageindex]
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.left, self.rect.top = 3 * self.rect.width, 2 * self.rect.height
        self._sound_drive = pygame.mixer.Sound(Settings.get_sound("tank_drive1.wav"))  # §\label{srcSound0101}§
        self._channel = pygame.mixer.find_channel()  # Sound-Kanal finden§\label{srcSound0104}§
        self.stereo()  # §\label{srcSound0102}§
        self._channel.play(self._sound_drive, -1)  # §\label{srcSound0103}§
        self._speed = 50

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "go" in kwargs.keys():
            if kwargs["go"]:
                self.update_imageindex()
                self.image = self._images[self._direction][self._imageindex]
                if self._direction == "up" or self._direction == "left":
                    self._speed = -50
                elif self._direction == "down" or self._direction == "right":
                    self._speed = 50
                if self._direction == "up" or self._direction == "down":
                    self.rect.move_ip(0, self._speed * Settings.DELTATIME)
                    if self.rect.top <= Settings.WINDOW.top:
                        self.turn("down")
                    if self.rect.bottom >= Settings.WINDOW.bottom:
                        self.turn("up")
                elif self._direction == "left" or self._direction == "right":
                    self.rect.move_ip(self._speed * Settings.DELTATIME, 0)
                    if self.rect.left <= Settings.WINDOW.left:
                        self.turn("right")
                    if self.rect.right >= Settings.WINDOW.right:
                        self.turn("left")
                self.stereo()
        if "turn" in kwargs.keys():
            self.turn(kwargs["turn"])

    def stereo(self) -> None:
        volume_rechts = self.rect.centerx / Settings.WINDOW.width  # §\label{srcSound0105}§
        volume_links = 1 - volume_rechts
        self._channel.set_volume(volume_links, volume_rechts)

    def turn(self, direction: str) -> None:
        self._direction = direction

    def update_imageindex(self) -> None:
        if self._speed == 0:
            self._imageindex = 0
        else:
            self._imageindex = (self._imageindex + 1) % len(self._images[self._direction])


class Bullet(pygame.sprite.Sprite):

    SOUND_FIRE = None  # Es braucht nur einen §\label{srcSound0106}§

    def __init__(self, tank: Tank) -> None:
        super().__init__()
        bulletspeed = 300
        number: dict[str, int] = {"left": 49, "right": 61, "up": 37, "down": 73}
        directions = {
            "left": pygame.Vector2(-bulletspeed, 0),
            "right": pygame.Vector2(bulletspeed, 0),
            "up": pygame.Vector2(0, -bulletspeed),
            "down": pygame.Vector2(0, bulletspeed),
        }
        fullfilename = os.path.join(Settings.PATH["image"], f"tankbrigade_part{number[tank._direction]}.png")
        self.image = pygame.image.load(fullfilename).convert()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self._direction = tank._direction
        self.rect.center = tank.rect.center
        self._speed = directions[tank._direction]

        if Bullet.SOUND_FIRE == None:  # Es braucht nur einen §\label{srcSound0107}§
            Bullet.SOUND_FIRE = pygame.mixer.Sound(Settings.get_sound("tank_fire1.wav"))
        volume_rechts = self.rect.centerx / Settings.WINDOW.width
        volume_links = 1 - volume_rechts
        self._channel: pygame.mixer.Channel = pygame.mixer.find_channel()
        self._channel.set_volume(volume_links, volume_rechts)
        self._channel.play(Bullet.SOUND_FIRE)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self._speed * Settings.DELTATIME)
        if not Settings.WINDOW.contains(self.rect):
            self.kill()


class Game:

    def __init__(self) -> None:
        pygame.init()
        self._window = pygame.Window(size=Settings.WINDOW.size, title="Steroeeffekt")
        self._screen = self._window.get_surface()
        self._clock = pygame.time.Clock()

        self._ground = pygame.sprite.GroupSingle(Ground())
        self._tankreference = Tank()
        self._tank = pygame.sprite.GroupSingle(self._tankreference)
        self._all_bullets = pygame.sprite.Group()
        self._running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_UP:
                    self._tank.update(turn="up")
                elif event.key == K_DOWN:
                    self._tank.sprite.update(turn="down")
                elif event.key == K_LEFT:
                    self._tank.sprite.update(turn="left")
                elif event.key == K_RIGHT:
                    self._tank.sprite.update(turn="right")
                elif event.key == K_SPACE:
                    self.fire()

    def fire(self) -> None:
        if len(self._all_bullets) < 5:
            self._all_bullets.add(Bullet(self._tankreference))

    def draw(self) -> None:
        self._ground.draw(self._screen)
        self._tank.draw(self._screen)
        self._all_bullets.draw(self._screen)
        self._window.flip()

    def update(self) -> None:
        self._tank.update(go=True)
        self._all_bullets.update()

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
