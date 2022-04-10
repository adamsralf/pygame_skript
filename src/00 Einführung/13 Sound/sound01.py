import os
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP,
                              KEYDOWN, QUIT)


class Settings:
    window: pygame.rect.Rect = pygame.rect.Rect(0, 0, 800, 160)
    fps = 60
    deltatime = 1.0/fps
    path: dict[str, str] = {}
    path["file"] = os.path.dirname(os.path.abspath(__file__))
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")

    @staticmethod
    def get_dim() -> Tuple[int, int]:
        return (Settings.window.width, Settings.window.height)

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.path["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.path["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.path["sound"], filename)


class Ground(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        fullfilename: str = Settings.get_image("tankbrigade_part64.png")
        tile: pygame.surface.Surface = pygame.image.load(fullfilename).convert()
        rect: pygame.rect.Rect = tile.get_rect()
        self.image: pygame.surface.Surface = pygame.Surface(Settings.get_dim())
        for row in range(Settings.window.width // rect.width):
            for col in range(Settings.window.height // rect.height):
                self.image.blit(tile, (row * rect.width, col * rect.height))
        self.rect: pygame.rect.Rect = self.image.get_rect()


class Tank(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image_filename = (209, 190, 202, 214, 226, 238, 250, 262)
        self.images: dict[str, list[pygame.surface.Surface]] = {"up": [], "down": [], "left": [], "right": []}
        for number in self.image_filename:
            fullfilename = Settings.get_image(f"tankbrigade_part{number}.png")
            picture = pygame.image.load(fullfilename).convert()
            picture.set_colorkey("black")
            self.images["up"].append(picture)
            self.images["down"].append(pygame.transform.rotate(picture, 180))
            self.images["left"].append(pygame.transform.rotate(picture, +90))
            self.images["right"].append(pygame.transform.rotate(picture, -90))
        self.direction: str = "right"
        self.imageindex: int = 0
        self.image: pygame.surface.Surface = self.images[self.direction][self.imageindex]
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.left, self.rect.top = 3 * self.rect.width, 2 * self.rect.height
        self.sound_drive: pygame.mixer.Sound = pygame.mixer.Sound(
            Settings.get_sound("tank_drive1.wav")
        )  # §\label{srcSound0101}§
        self.channel: pygame.mixer.Channel = pygame.mixer.find_channel()  # Sound-Kanal finden§\label{srcSound0104}§
        self.stereo()  # §\label{srcSound0102}§
        self.channel.play(self.sound_drive, -1)  # §\label{srcSound0103}§
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = 50

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "go" in kwargs.keys():
            if kwargs["go"]:
                self.update_imageindex()
                self.image = self.images[self.direction][self.imageindex]
                if self.direction == "up" or self.direction == "left":
                    self.speed = -50
                elif self.direction == "down" or self.direction == "right":
                    self.speed = 50
                if self.direction == "up" or self.direction == "down":
                    self.position.y += (self.speed * Settings.deltatime)
                    self.rect.top = round(self.position.y)
                    if self.rect.top <= self.rect.height // 2:
                        self.turn("down")
                    if self.rect.bottom >= Settings.window.height - self.rect.height // 2:
                        self.turn("up")
                elif self.direction == "left" or self.direction == "right":
                    self.position.x += (self.speed * Settings.deltatime)
                    self.rect.left = round(self.position.x)
                    if self.rect.left <= self.rect.width // 2:
                        self.turn("right")
                    if self.rect.right >= Settings.window.width - self.rect.width // 2:
                        self.turn("left")
                self.stereo()
        if "turn" in kwargs.keys():
            self.turn(kwargs["turn"])

    def stereo(self) -> None:
        volume_rechts = self.rect.centerx / Settings.window.width  # §\label{srcSound0105}§
        volume_links = 1 - volume_rechts
        self.channel.set_volume(volume_links, volume_rechts)

    def turn(self, direction: str) -> None:
        self.direction = direction

    def update_imageindex(self) -> None:
        if self.speed == 0:
            self.imageindex = 0
        else:
            self.imageindex = (self.imageindex + 1) % len(self.images[self.direction])


class Bullet(pygame.sprite.Sprite):

    _sound_fire = None  # Es braucht nur einen §\label{srcSound0106}§

    def __init__(self, tank: Tank) -> None:
        super().__init__()
        bulletspeed = 300
        number: dict[str, int] = {"left": 49, "right": 61, "up": 37, "down": 73}
        directions = {
            "left": (-bulletspeed, 0),
            "right": (bulletspeed, 0),
            "up": (0, -bulletspeed),
            "down": (0, bulletspeed),
        }
        fullfilename = os.path.join(Settings.path["image"], f"tankbrigade_part{number[tank.direction]}.png")
        self.image: pygame.surface.Surface = pygame.image.load(fullfilename).convert()
        self.image.set_colorkey("black")
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.direction = tank.direction
        self.rect.center = tank.rect.center
        self.speed: Tuple[int, int] = directions[tank.direction]
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)

        if Bullet._sound_fire == None:                  # Es braucht nur einen §\label{srcSound0107}§
            Bullet._sound_fire = pygame.mixer.Sound(Settings.get_sound("tank_fire1.wav"))
        volume_rechts = self.rect.centerx / Settings.window.width
        volume_links = 1 - volume_rechts
        self.channel: pygame.mixer.Channel = pygame.mixer.find_channel()
        self.channel.set_volume(volume_links, volume_rechts)
        self.channel.play(Bullet._sound_fire)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.position.x += self.speed[0] * Settings.deltatime
        self.rect.left = round(self.position.x)
        self.position.y += self.speed[1] * Settings.deltatime
        self.rect.top = round(self.position.y)
        if self.rect.right <= 0:
            self.kill()
        elif self.rect.left >= Settings.window.width:
            self.kill()
        elif self.rect.bottom <= 0:
            self.kill()
        elif self.rect.top >= Settings.window.height:
            self.kill()


class Game:

    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption("Steroeeffekt")
        self.clock = pygame.time.Clock()
        self.ground = pygame.sprite.GroupSingle(Ground())
        self.tankreference = Tank()
        self.tank = pygame.sprite.GroupSingle(self.tankreference)
        self.all_bullets = pygame.sprite.Group()
        self.running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_UP:
                    self.tank.update(turn="up")
                elif event.key == K_DOWN:
                    self.tank.sprite.update(turn="down")
                elif event.key == K_LEFT:
                    self.tank.sprite.update(turn="left")
                elif event.key == K_RIGHT:
                    self.tank.sprite.update(turn="right")
                elif event.key == K_SPACE:
                    self.fire()

    def fire(self) -> None:
        if len(self.all_bullets) < 5:
            self.all_bullets.add(Bullet(self.tankreference))

    def draw(self) -> None:
        self.ground.draw(self._screen)
        self.tank.draw(self._screen)
        self.all_bullets.draw(self._screen)
        pygame.display.flip()

    def update(self) -> None:
        self.tank.update(go=True)
        self.all_bullets.update()

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.fps)
            time_current = time()
            Settings.deltatime = time_current - time_previous
            time_previous = time_current
        pygame.quit()


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
