from random import choice, randint
from typing import Any

import pygame
from globals import Settings


class Tile(pygame.sprite.Sprite):
    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__()
        self.image = pygame.Surface(Settings.TILESIZE_WORLD)
        # Yellow -> White according to the distance to the center§\label{tilev0101}§
        v1 = pygame.Vector2(position)
        v2 = pygame.Vector2(Settings.WORLD.center)
        distance = v2.distance_to(v1)
        max_distance = v2.length()
        rel_dist_center = min(1.0, distance / max_distance)
        blue_value = int(255 * (1 - rel_dist_center))       #§\label{tilev0102}§
        color = (255, 255, blue_value)
        self.image.fill(color)
        if Settings.TILE_WITH_BORDER > 0:
            pygame.draw.rect(self.image, "Black", 
                             ((0,0), Settings.TILESIZE_WORLD), 
                             Settings.TILE_WITH_BORDER)
        self.rect = self.image.get_rect(topleft=position)
   

class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__()
        self.image : pygame.surface.Surface = pygame.surface.Surface(Settings.TILESIZE_WORLD)
        self.image.set_colorkey((0, 0, 0))

        self.radius = int(Settings.TILESIZE_WORLD.x // 2)
        pygame.draw.circle(self.image, "red", (self.radius, self.radius), self.radius)
        self.rect : pygame.rect.FRect = self.image.get_frect(center=position)

        self.speed = 400.0  # pixels per second
        self.directions = {
            "left": pygame.Vector2(-1, 0),
            "right": pygame.Vector2(1, 0),
            "up": pygame.Vector2(0, -1),
            "down": pygame.Vector2(0, 1),
            "stop": pygame.Vector2(0, 0),
        }
        self.direction = self.directions["stop"]

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "position" in kwargs:
            self.rect.center = kwargs["position"]
        if "move" in kwargs:
            self.direction = self.directions[kwargs["move"]]
        new_position = pygame.Vector2(self.rect.center) + self.direction * (
            self.speed * Settings.DELTATIME
        )
        self.rect.center = new_position
        self.rect.clamp_ip(Settings.WORLD)
        return super().update(*args, **kwargs)


class Mob(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        x1 = int(Settings.TILESIZE_WORLD.x + 10)
        x2 = int(Settings.WORLD.width - (Settings.TILESIZE_WORLD.x + 10))
        y1 = int(Settings.TILESIZE_WORLD.y + 10)
        y2 = int(Settings.WORLD.height - (Settings.TILESIZE_WORLD.y + 10))
        position = (randint(x1, x2), randint(y1, y2))
        self.image = pygame.Surface(Settings.TILESIZE_WORLD, pygame.SRCALPHA)
        color = (0, 0, randint(10, 255))
        pad = randint(0, int(Settings.TILESIZE_WORLD.x//2 - 1))
        pygame.draw.rect(self.image, 
                         color, 
                         ((pad,pad), (Settings.TILESIZE_WORLD.x - 2*pad, 
                                      Settings.TILESIZE_WORLD.y - 2*pad)))
        self.rect = self.image.get_frect()
        self.rect.topleft = position
        self.direction = pygame.Vector2(choice((-1, 1)), choice((-1,1)))
        self.speed = randint(100, 500) # px/sec

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.direction * self.speed * Settings.DELTATIME)
        if self.rect.right < Settings.WORLD.left:
            self.rect.left = Settings.WORLD.right
        elif self.rect.left > Settings.WORLD.right:
            self.rect.right = Settings.WORLD.left
        if self.rect.bottom < Settings.WORLD.top:
            self.rect.top = Settings.WORLD.bottom
        elif self.rect.top > Settings.WORLD.bottom:
            self.rect.bottom = Settings.WORLD.top
        return super().update(*args, **kwargs)

