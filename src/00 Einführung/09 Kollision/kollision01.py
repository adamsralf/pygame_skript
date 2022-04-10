import os
from typing import Any, Tuple

import pygame


class Settings(object):

    window = {'width': 700, 'height': 200}
    fps = 60
    title = "Kollisionsarten"
    path: dict[str, str] = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    modus = "rect"

    @staticmethod
    def dim() -> Tuple[int, int]:
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name: str) -> str:
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name: str) -> str:
        return os.path.join(Settings.path['image'], name)


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, filename1: str, filename2: str) -> None:
        super().__init__()
        self.image_normal: pygame.surface.Surface = pygame.image.load(Settings.imagepath(filename1)).convert_alpha()
        self.image_hit: pygame.surface.Surface = pygame.image.load(Settings.imagepath(filename2)).convert_alpha()
        self.image = self.image_normal
        self.rect: pygame.rect.Rect = self.image.get_rect()  # Rechteck §\label{srcKollision01}§
        self.mask = pygame.mask.from_surface(self.image)     # Maske §\label{srcKollision02}§
        self.radius = self.rect.width // 2                   # Innenkreis §\label{srcKollision03}§
        self.rect.centery = Settings.window['height'] // 2
        self.hit = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "hit" in kwargs.keys():
            self.hit = kwargs["hit"]
        self.image = self.image_hit if (self.hit) else self.image_normal


class Bullet(pygame.sprite.Sprite):

    def __init__(self, picturefile: str) -> None:
        super().__init__()
        self.image: pygame.surface.Surface = pygame.image.load(Settings.imagepath(picturefile)).convert_alpha()
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (10, 10)
        self.directions = {'stop': (0, 0), 'down': (0,  1),
                           'up': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
        self.set_direction('stop')

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
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode(Settings.dim())
        self.clock = pygame.time.Clock()
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
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.bullet.sprite.update(direction='down')
                elif event.key == pygame.K_UP:
                    self.bullet.sprite.update(direction='up')
                elif event.key == pygame.K_LEFT:
                    self.bullet.sprite.update(direction='left')
                elif event.key == pygame.K_RIGHT:
                    self.bullet.sprite.update(direction='right')
                elif event.key == pygame.K_r:
                    Settings.modus = "rect"
                elif event.key == pygame.K_c:
                    Settings.modus = "circle"
                elif event.key == pygame.K_m:
                    Settings.modus = "mask"
            elif event.type == pygame.KEYUP:
                self.bullet.sprite.update(direction='stop')

    def update(self) -> None:
        self.check_for_collision()
        self.bullet.update(action="move")
        self.all_obstacles.update()

    def draw(self) -> None:
        self.screen.fill("white")
        self.all_obstacles.draw(self.screen)
        self.bullet.draw(self.screen)
        text_surface_modus = self.font.render(f"Modus: {Settings.modus}", True, "blue")
        self.screen.blit(text_surface_modus, dest=(10, Settings.window['height']-30))
        pygame.display.flip()

    def resize(self) -> None:
        total_width = 0
        for s in self.all_obstacles:
            total_width += s.rect.width
        padding = (Settings.window['width'] - total_width) // 4     # Abstand §\label{srcKollision04}§
        for i in range(len(self.all_obstacles)):
            if i == 0:
                self.all_obstacles.sprites()[i].rect.left = padding
            else:
                self.all_obstacles.sprites()[i].rect.left = self.all_obstacles.sprites()[i-1].rect.right + padding

    def check_for_collision(self) -> None:
        match Settings.modus:
            case "circle":
                func = pygame.sprite.collide_circle
            case "mask":
                func = pygame.sprite.collide_mask
            case _:
                func = pygame.sprite.collide_rect
        hits = pygame.sprite.spritecollide(self.bullet.sprite, self.all_obstacles, False, func)
        for s in self.all_obstacles:
            s.update(hit=s in hits)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
