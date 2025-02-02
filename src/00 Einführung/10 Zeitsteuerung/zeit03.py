import os
from time import time
from typing import Any, Tuple

import pygame


class Settings(object):
    WINDOW = pygame.rect.Rect((0, 0), (700, 200))
    FPS = 60
    DELTATIME = 1.0 / FPS
    TITLE = "Zeitsteuerung"
    PATH: dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")

    @staticmethod
    def filepath(name: str) -> str:
        return os.path.join(Settings.PATH["file"], name)

    @staticmethod
    def imagepath(name: str) -> str:
        return os.path.join(Settings.PATH["image"], name)


class Timer(object):

    def __init__(self, duration: int, with_start: bool = True) -> None:
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False


class Enemy(pygame.sprite.Sprite):

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.topleft = (10, 10)
        self.direction = 1
        self.speed = pygame.math.Vector2(150, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        newpos = self.rect.move(self.speed * Settings.DELTATIME * self.direction)
        if newpos.left < 10 or newpos.right >= Settings.WINDOW.right - 10:
            self.direction *= -1
        else:
            self.rect = newpos


class Bullet(pygame.sprite.Sprite):

    def __init__(self, picturefile: str, startpos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(picturefile)).convert_alpha()
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.center = startpos
        self.direction = 1
        self.speed = pygame.math.Vector2(0, 100)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.speed * Settings.DELTATIME * self.direction)
        if self.rect.top > Settings.WINDOW.bottom - 30:
            self.kill()


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=Settings.WINDOW.size, title=Settings.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.enemy = pygame.sprite.GroupSingle(Enemy("alienbig1.png"))
        self.all_bullets = pygame.sprite.Group()
        self.bullet_timer = Timer(500)  # Timer ohne Verzögerung§\label{srcZeit0301}§
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
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
        self.window.flip()

    def update(self) -> None:
        self.new_bullet()
        self.all_bullets.update()
        self.enemy.update()

    def new_bullet(self) -> None:
        if self.bullet_timer.is_next_stop_reached():  # Wenn Intervallgrenze erreicht§\label{srcZeit0302}§
            self.all_bullets.add(Bullet("shoot.png", self.enemy.sprite.rect.move(0, 20).center))


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
