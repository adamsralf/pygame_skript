import os
from typing import Any

import pygame


class Settings(object):

    WINDOW = pygame.rect.Rect((0, 0), (700, 200))
    FPS = 60
    TITLE = "Kollisionsarten"
    PATH: dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    MODUS = "rect"

    @staticmethod
    def filepath(name: str) -> str:
        return os.path.join(Settings.PATH["file"], name)

    @staticmethod
    def imagepath(name: str) -> str:
        return os.path.join(Settings.PATH["image"], name)


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, filename1: str, filename2: str) -> None:
        super().__init__()
        self.image_normal = pygame.image.load(Settings.imagepath(filename1)).convert_alpha()
        self.image_hit = pygame.image.load(Settings.imagepath(filename2)).convert_alpha()
        self.image = self.image_normal
        self.rect = self.image.get_rect()  # Rechteck §\label{srcKollision01}§
        self.mask = pygame.mask.from_surface(self.image)  # Maske §\label{srcKollision02}§
        self.radius = self.rect.centerx  # Innenkreis §\label{srcKollision03}§
        self.rect.centery = Settings.WINDOW.centery
        self.hit = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "hit" in kwargs.keys():
            self.hit = kwargs["hit"]
        self.image = self.image_hit if (self.hit) else self.image_normal


class Bullet(pygame.sprite.Sprite):

    def __init__(self, picturefile: str) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(picturefile)).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = self.rect.centery
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (10, 10)
        self.directions = {"stop": (0, 0), "down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0)}
        self.set_direction("stop")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.rect.move_ip(self.speed)
        elif "direction" in kwargs.keys():
            self.set_direction(kwargs["direction"])

    def set_direction(self, direction: str) -> None:
        self.speed = self.directions[direction]


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=Settings.WINDOW.size, title=Settings.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.bullet = pygame.sprite.GroupSingle(Bullet("shoot.png"))
        self.all_obstacles = pygame.sprite.Group()
        self.all_obstacles.add(Obstacle("brick1.png", "brick2.png"))
        self.all_obstacles.add(Obstacle("raumschiff1.png", "raumschiff2.png"))
        self.all_obstacles.add(Obstacle("alienbig1.png", "alienbig2.png"))
        self.running = False

    def run(self) -> None:
        self.resize()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.bullet.sprite.update(direction="down")
                elif event.key == pygame.K_UP:
                    self.bullet.sprite.update(direction="up")
                elif event.key == pygame.K_LEFT:
                    self.bullet.sprite.update(direction="left")
                elif event.key == pygame.K_RIGHT:
                    self.bullet.sprite.update(direction="right")
                elif event.key == pygame.K_r:
                    Settings.MODUS = "rect"
                elif event.key == pygame.K_c:
                    Settings.MODUS = "circle"
                elif event.key == pygame.K_m:
                    Settings.MODUS = "mask"
            elif event.type == pygame.KEYUP:
                self.bullet.sprite.update(direction="stop")

    def update(self) -> None:
        self.check_for_collision()
        self.bullet.update(action="move")
        self.all_obstacles.update()

    def draw(self) -> None:
        self.screen.fill("white")
        self.all_obstacles.draw(self.screen)
        self.bullet.draw(self.screen)
        text_surface_modus = self.font.render(f"Modus: {Settings.MODUS}", True, "blue")
        self.screen.blit(text_surface_modus, dest=(10, Settings.WINDOW.bottom - 30))
        self.window.flip()

    def resize(self) -> None:
        total_width = 0
        for s in self.all_obstacles:
            total_width += s.rect.width
        padding = (Settings.WINDOW.width - total_width) // 4  # Abstand §\label{srcKollision04}§
        for i in range(len(self.all_obstacles)):
            if i == 0:
                self.all_obstacles.sprites()[i].rect.left = padding
            else:
                self.all_obstacles.sprites()[i].rect.left = self.all_obstacles.sprites()[i - 1].rect.right + padding

    def check_for_collision(self) -> None:
        if Settings.MODUS == "circle":
            for s in self.all_obstacles:
                s.update(hit=pygame.sprite.collide_circle(self.bullet.sprite, s))
        elif Settings.MODUS == "mask":
            for s in self.all_obstacles:
                s.update(hit=pygame.sprite.collide_mask(self.bullet.sprite, s))
        else:
            for s in self.all_obstacles:
                s.update(hit=pygame.sprite.collide_rect(self.bullet.sprite, s))


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
