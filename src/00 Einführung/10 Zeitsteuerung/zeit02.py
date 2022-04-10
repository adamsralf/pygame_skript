import os
from time import time
from typing import Any, Tuple

import pygame


class Settings(object):
    window = {'width': 700, 'height': 200}
    fps = 60
    deltatime = 1.0 / fps
    title = "Zeitsteuerung"
    path: dict[str, str] = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")

    @staticmethod
    def dim() -> Tuple[int, int]:
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name: str) -> str:
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name: str) -> str:
        return os.path.join(Settings.path['image'], name)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = (10, 10)
        self.direction = 1
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = pygame.math.Vector2(150, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        newpos = self.position + (self.speed * Settings.deltatime * self.direction)
        self.rect.left = round(newpos.x)
        if self.rect.left < 10 or self.rect.right >= Settings.window['width'] - 10:
            self.direction *= -1
        self.position += (self.speed * Settings.deltatime * self.direction)
        self.rect.left = round(self.position.x)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, picturefile: str, startpos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(picturefile)).convert_alpha()
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = startpos
        self.direction = 1
        self.position = pygame.math.Vector2(self.rect.left, self.rect.top)
        self.speed = pygame.math.Vector2(0, 100)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.position += (self.speed * Settings.deltatime * self.direction)
        self.rect.top = round(self.position.y)
        if self.rect.top > Settings.window['height'] - 30:
            self.kill()


class Game(object):

    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.screen = pygame.display.set_mode(Settings.dim())
        self.clock = pygame.time.Clock()
        self.enemy = pygame.sprite.GroupSingle(Enemy("alienbig1.png"))
        self.all_bullets = pygame.sprite.Group()
        self.time_stamp = pygame.time.get_ticks()          # Zeitpunkt festhalten§\label{srcZeit0201}§
        self.time_duration = 500                           # Intervalldauer§\label{srcZeit0202}§
        self.running = False

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

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.all_bullets.draw(self.screen)
        self.enemy.draw(self.screen)
        pygame.display.flip()

    def update(self) -> None:
        self.new_bullet()
        self.all_bullets.update()
        self.enemy.update()

    def new_bullet(self) -> None:
        if pygame.time.get_ticks() >= self.time_stamp + self.time_duration:  # Intervallgrenze?§\label{srcZeit0204}§
            self.all_bullets.add(Bullet("shoot.png", self.enemy.sprite.rect.move(0, 20).center))
            self.time_stamp = pygame.time.get_ticks()                        # Intervallstart §\label{srcZeit0205}§


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
