from random import choice, randrange
from time import time
from typing import Any, Tuple

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    DELTATIME = 1.0 / FPS


class MyEvents:
    POINT_FOR = pygame.USEREVENT
    MYEVENT = pygame.event.Event(POINT_FOR, player=0)


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.surface.Surface(Settings.WINDOW.size).convert()
        self.rect = self.image.get_rect()
        self.image.fill("darkred")
        self._paint_net()

    def _paint_net(self) -> None:
        net_rect = pygame.rect.Rect(0, 0, 0, 0)
        net_rect.centerx = Settings.WINDOW.centerx
        net_rect.top = 50
        net_rect.size = (3, 30)
        while net_rect.bottom < Settings.WINDOW.bottom:
            pygame.draw.rect(self.image, "grey", net_rect, 0)
            net_rect.move_ip(0, 40)


class Paddle(pygame.sprite.Sprite):
    BORDERDISTANCE = {"horizontal": 50, "vertical": 10}
    DIRECTION = {"up": -1, "down": 1, "halt": 0}

    def __init__(self, player: str, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 15, Settings.WINDOW.height // 10)
        self.rect.centery = Settings.WINDOW.centery
        self._player = player
        if self._player == "left":
            self.rect.left = Paddle.BORDERDISTANCE["horizontal"]
        else:
            self.rect.right = Settings.WINDOW.right - Paddle.BORDERDISTANCE["horizontal"]
        self._speed = Settings.WINDOW.height // 2
        self._direction = Paddle.DIRECTION["halt"]  # Steht erstmal still
        self.image = pygame.surface.Surface(self.rect.size)
        self.image.fill("yellow")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] in Paddle.DIRECTION.keys():
                self._direction = Paddle.DIRECTION[kwargs["action"]]
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        if self._direction != Paddle.DIRECTION["halt"]:
            self.rect.move_ip(0, self._speed * self._direction * Settings.DELTATIME)
            if self._direction == Paddle.DIRECTION["up"]:
                self.rect.top = max(self.rect.top, Paddle.BORDERDISTANCE["vertical"])
            elif self._direction == Paddle.DIRECTION["down"]:
                self.rect.bottom = min(self.rect.bottom, Settings.WINDOW.height - Paddle.BORDERDISTANCE["vertical"])


class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 20, 20)
        self.image = pygame.surface.Surface(self.rect.size).convert()
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, "green", self.rect.center, self.rect.width // 2)
        self._speed = Settings.WINDOW.width // 3
        self._speedxy = pygame.Vector2()
        self._service()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] == "hflip":
                self._horizontal_flip()
            elif kwargs["action"] == "vflip":
                self._vertical_flip()
            elif kwargs["action"] == "reset":
                self._service()
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        self.rect.move_ip(self._speedxy * Settings.DELTATIME)
        if self.rect.top <= 0:
            self._vertical_flip()
            self.rect.top = 0
        elif self.rect.bottom >= Settings.WINDOW.bottom:
            self._vertical_flip()
            self.rect.bottom = Settings.WINDOW.bottom
        elif self.rect.right < 0:
            MyEvents.MYEVENT.player = 2
            pygame.event.post(MyEvents.MYEVENT)
            self._service()
        elif self.rect.left > Settings.WINDOW.right:
            MyEvents.MYEVENT.player = 1
            pygame.event.post(MyEvents.MYEVENT)
            self._service()

    def _service(self) -> None:
        self.rect.center = Settings.WINDOW.center
        self._speedxy = pygame.Vector2(choice([-1, 1]), choice([-1, 1])) * self._speed

    def _horizontal_flip(self) -> None:
        self._speedxy.x *= -1
        self._respeed()

    def _vertical_flip(self) -> None:
        self._speedxy.y *= -1

    def _respeed(self) -> None:
        self._speedxy.x += randrange(0, self._speed // 4)
        self._speedxy.y += randrange(0, self._speed // 4)


class Score(pygame.sprite.Sprite):

    def __init__(self, *groups: Tuple[pygame.sprite.Group]):
        super().__init__(*groups)
        self._font = pygame.font.SysFont(None, 30)
        self._score = {1: 0, 2: 0}
        self.image: pygame.surface.Surface = None
        self.rect: pygame.rect.Rect = None
        self._render()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "player" in kwargs.keys():
            self._score[kwargs["player"]] += 1
            self._render()
        return super().update(*args, **kwargs)

    def _render(self):
        self.image = self._font.render(f"{self._score[1]} : {self._score[2]}", True, "white")
        self.rect = self.image.get_rect(centerx=Settings.WINDOW.centerx, top=15)


class Game:
    def __init__(self):
        self._window = pygame.Window(size=Settings.WINDOW.size, title="My Kind of Pong", position=pygame.WINDOWPOS_CENTERED)
        self._screen = self._window.get_surface()
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
        self._all_sprites = pygame.sprite.Group()
        self._paddle = {}
        self._paddle["left"] = Paddle("left", self._all_sprites)
        self._paddle["right"] = Paddle("right", self._all_sprites)
        self._ball = Ball(self._all_sprites)
        self._score = Score(self._all_sprites)
        self._running = True

    def run(self):
        time_previous = time()
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def update(self):
        self._check_collision()
        self._all_sprites.update(action="move")

    def draw(self):
        self._background.draw(self._screen)
        self._all_sprites.draw(self._screen)
        self._window.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_UP:
                    self._paddle["right"].update(action="up")
                elif event.key == pygame.K_DOWN:
                    self._paddle["right"].update(action="down")
                elif event.key == pygame.K_w:
                    self._paddle["left"].update(action="up")
                elif event.key == pygame.K_s:
                    self._paddle["left"].update(action="down")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self._paddle["right"].update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self._paddle["left"].update(action="halt")
            elif event.type == MyEvents.POINT_FOR:
                self._score.update(player=event.player)

    def _check_collision(self):
        if pygame.sprite.collide_rect(self._ball, self._paddle["left"]):
            self._ball.update(action="hflip")
            self._ball.rect.left = self._paddle["left"].rect.right + 1
        elif pygame.sprite.collide_rect(self._ball, self._paddle["right"]):
            self._ball.update(action="hflip")
            self._ball.rect.right = self._paddle["right"].rect.left - 1


def main():
    Game().run()


if __name__ == "__main__":
    main()
