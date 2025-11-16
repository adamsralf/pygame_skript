from typing import Tuple, Union

import pygame
from globals import Settings

Vec2Like = Union[pygame.Vector2, Tuple[float, float]]

class WindowPlain:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (0 * (Settings.WINDOW.width + 60), 
                                0 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Plain Window (size={self.rect.size})"
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        a = [r for r in self.tiles.sprites() if Settings.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        a = [r for r in self.mobs.sprites() if Settings.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "plain_image.png")


class WindowBirdEyeView:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.zoom = Settings.ZOOM_BIRDEYE
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (1 * (Settings.WINDOW.width + 60), 
                                0 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Birdeye (zoom=({self.zoom.x:0.2f}, {self.zoom.y:0.2f})"
        self.clock = pygame.time.Clock()

    def draw(self, rects:list):
        for sprite in self.tiles:
            self.screen.blit(sprite.image_small, self.zoom_rect(sprite.rect))
        for sprite in self.mobs:
            self.screen.blit(sprite.image_small, self.zoom_rect(sprite.rect))
        if rects:       # Are rects to draw?
            for item in rects:
                pygame.draw.rect(self.screen, item["color"], self.zoom_rect(item["rect"]), 2)
        self.window.flip()

    def zoom_rect(self, rect: Union[pygame.rect.Rect, pygame.rect.FRect]) -> pygame.rect.FRect:
        x = rect.x * self.zoom.x
        y = rect.y * self.zoom.y
        w = rect.w * self.zoom.x
        h = rect.h * self.zoom.y
        return pygame.rect.FRect(x, y, w, h)

    def save(self):
        pygame.image.save(self.screen, "birdeye_image.png")


class WindowCenteredCamera:

    def __init__(self, player:pygame.sprite.Sprite, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.player = player
        self.offset = pygame.Vector2(0, 0) #
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (2 * (Settings.WINDOW.width + 60), 
                                0 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        w = self.camera2world(Settings.WINDOW)
        a = [r for r in self.tiles.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect)) 
        a = [r for r in self.mobs.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect))
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "centered_image.png")

    def scroll(self) -> None:
        self.offset.x = max(0, self.player.rect.x - self.rect.width / 2)
        self.offset.y = max(0, self.player.rect.y - self.rect.height / 2)
        self.offset.x = min(Settings.WORLD.right - self.rect.width, self.offset.x)
        self.offset.y = min(Settings.WORLD.bottom - self.rect.height, self.offset.y)

        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft + self.offset, rect.size)


class WindowPagewise:

    def __init__(self, player:pygame.sprite.Sprite, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group, padding:int = 1) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.player = player
        self.offset = pygame.Vector2(0, 0) 
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (0 * (Settings.WINDOW.width + 60), 
                                1 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.clock = pygame.time.Clock()
        self.inner_rect = pygame.rect.FRect(
            Settings.WINDOW.left + padding * player.rect.width,
            Settings.WINDOW.top + padding * player.rect.height,
            Settings.WINDOW.width - padding * 2 * player.rect.width,
            Settings.WINDOW.height - padding * 2 * player.rect.height,
        )

    def draw(self):
        self.screen.fill("Black")
        w = self.camera2world(Settings.WINDOW)
        a = [r for r in self.tiles.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect)) 
        a = [r for r in self.mobs.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect))
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "pagewise_image.png")

    def scroll(self) -> None:
        m = self.camera2world(self.inner_rect)
        player_in_view = self.world2camera(self.player.rect)
        if not player_in_view.colliderect(self.inner_rect):     # nicht mehr innerhalb?
            self.offset.x = max(0, self.player.rect.x - Settings.WINDOW.centerx)
            self.offset.y = max(0, self.player.rect.y - Settings.WINDOW.centery)
            self.offset.x = min(Settings.WORLD.right - Settings.WINDOW.width, self.offset.x)
            self.offset.y = min(Settings.WORLD.bottom - Settings.WINDOW.height, self.offset.y)
        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft + self.offset, rect.size)


class WindowAuto:

    def __init__(self, player:pygame.sprite.Sprite, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group, direction:Vec2Like) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.player = player
        self.offset = pygame.Vector2(0, 0) #
        self.window = pygame.Window(size=Settings.WINDOW.size)
        self.window.position = (1 * (Settings.WINDOW.width + 60), 
                                1 * (Settings.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.direction = pygame.math.Vector2(direction)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        w = self.camera2world(Settings.WINDOW)
        a = [r for r in self.tiles.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect)) 
        a = [r for r in self.mobs.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect))
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "auto_image.png")

    def scroll(self) -> None:
        self.offset += self.direction * Settings.DELTATIME
        self.offset.x = max(0, self.offset.x)
        self.offset.y = max(0, self.offset.y)
        self.offset.x = min(Settings.WORLD.right - Settings.WINDOW.width, self.offset.x)
        self.offset.y = min(Settings.WORLD.bottom - Settings.WINDOW.height, self.offset.y)

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft + self.offset, rect.size)


