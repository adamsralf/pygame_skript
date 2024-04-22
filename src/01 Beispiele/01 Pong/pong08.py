import os
from random import choice, randint
from time import time
from typing import Any, Tuple

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    DELTATIME = 1.0 / FPS
    KI = {"left": False, "right": False}
    SOUNDFLAG = True
    PATH = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["sound"] = os.path.join(PATH["file"], "sounds")

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.PATH["sound"], filename)


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


class Pause(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(Settings.WINDOW.topleft, Settings.WINDOW.size)
        self.image = pygame.surface.Surface(self.rect.size).convert_alpha()
        self.image.fill([120, 120, 120, 200])  # transparentes Grau§\label{srcPong0801}§


class Help(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(Settings.WINDOW.topleft, Settings.WINDOW.size)
        self.image = pygame.surface.Surface(self.rect.size).convert_alpha()
        self.image.fill([20, 20, 20, 200])  # transparentes Grau§\label{srcPong0802}§
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text_l = "h\np\nESC\n\nF2\nk\nl\nr\n\nUP\nDOWN\nw\ns"
        text_r = "- toogle help modus\n- toogle pause modus\n- quit\n\n- toogle sound modus\n"
        text_r += "- toogle both paddles KI modus\n- toogle left paddle KI modus\n- toogle right paddle KI modus\n\n"
        text_r += "- left paddle move up\n- left paddle move down\n- right paddle move up\n- right paddle move down"
        lines = font.render(text_l, True, "white")
        self.image.blit(lines, (10, 10))
        lines = font.render(text_r, True, "white")
        self.image.blit(lines, (10 + 70, 10))


class Paddle(pygame.sprite.Sprite):
    BORDERDISTANCE = {"horizontal": 50, "vertical": 10}
    DIRECTION = {"up": -1, "down": 1, "halt": 0}

    def __init__(self, player: str, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 15, Settings.WINDOW.height // 10)
        self.rect.centery = Settings.WINDOW.centery
        self._images = {
            "byhand": pygame.surface.Surface(self.rect.size).convert(),
            "byki": pygame.surface.Surface(self.rect.size).convert(),
        }
        self._images["byhand"].fill("yellow")
        self._images["byki"].fill("deepskyblue2")
        self._player = player
        if self._player == "left":
            self.rect.left = Paddle.BORDERDISTANCE["horizontal"]
        else:
            self.rect.right = Settings.WINDOW.right - Paddle.BORDERDISTANCE["horizontal"]
        self._speed = Settings.WINDOW.height // 2
        self._direction = Paddle.DIRECTION["halt"]
        self._select_image()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] in Paddle.DIRECTION.keys():
                self._direction = Paddle.DIRECTION[kwargs["action"]]
        self._select_image()
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        if self._direction != Paddle.DIRECTION["halt"]:
            self.rect.move_ip(0, self._speed * self._direction * Settings.DELTATIME)
            if self._direction == Paddle.DIRECTION["up"]:
                self.rect.top = max(self.rect.top, Paddle.BORDERDISTANCE["vertical"])
            elif self._direction == Paddle.DIRECTION["down"]:
                self.rect.bottom = min(self.rect.bottom, Settings.WINDOW.height - Paddle.BORDERDISTANCE["vertical"])

    def _select_image(self) -> None:
        if self._player == "left":
            if Settings.KI["left"]:
                self.image = self._images["byki"]
            else:
                self.image = self._images["byhand"]
        else:
            if Settings.KI["right"]:
                self.image = self._images["byki"]
            else:
                self.image = self._images["byhand"]


class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._sounds["left"] = pygame.mixer.Sound(Settings.get_sound("playerl.mp3"))
        self._sounds["right"] = pygame.mixer.Sound(Settings.get_sound("playerr.mp3"))
        self._sounds["bounce"] = pygame.mixer.Sound(Settings.get_sound("bounce.mp3"))
        self._channel = pygame.mixer.find_channel()
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
        if Settings.SOUNDFLAG:
            if self._speedxy.x < 0:
                self._channel.set_volume(0.9, 0.1)
                self._channel.play(self._sounds["left"])
            else:
                self._channel.set_volume(0.1, 0.9)
                self._channel.play(self._sounds["right"])
        self._speedxy.x *= -1
        self._respeed()

    def _vertical_flip(self) -> None:
        if Settings.SOUNDFLAG:
            rel_pos = self.rect.centerx / Settings.WINDOW.width
            self._channel.set_volume(1.0 - rel_pos, rel_pos)
            self._channel.play(self._sounds["bounce"])
        self._speedxy.y *= -1

    def _respeed(self) -> None:
        self._speedxy.x += randint(0, self._speed // 4)
        self._speedxy.y += randint(0, self._speed // 4)


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
        pygame.init()
        self._display = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("My Kind of Pong")
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
        self._all_sprites = pygame.sprite.Group()
        self._paddle = {}
        self._paddle["left"] = Paddle("left", self._all_sprites)
        self._paddle["right"] = Paddle("right", self._all_sprites)
        self._ball = Ball(self._all_sprites)
        self._score = Score(self._all_sprites)
        self._running = True
        self._pausing = False  # Pause Flag§\label{srcPong0803}§
        self._helping = False  # Hilfe Flag§\label{srcPong0804}§
        self._pause = pygame.sprite.GroupSingle(Pause())
        self._help = pygame.sprite.GroupSingle(Help())

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
        if not (self._pausing or self._helping):  # Nur bei Normalbetrieb§\label{srcPong0805}§
            self._check_collision()
            for i in Settings.KI.keys():
                if Settings.KI[i]:
                    self._paddlecontroler(self._paddle[i])
            self._all_sprites.update(action="move")

    def draw(self):
        self._background.draw(self._display)
        self._all_sprites.draw(self._display)
        if self._pausing:  # Pausedarstellung§\label{srcPong0806}§
            self._pause.draw(self._display)
        elif self._helping:  # Hilfedarstellung§\label{srcPong0807}§
            self._help.draw(self._display)
        pygame.display.update()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_UP:
                    if not Settings.KI["right"]:
                        self._paddle["right"].update(action="up")
                elif event.key == pygame.K_DOWN:
                    if not Settings.KI["right"]:
                        self._paddle["right"].update(action="down")
                elif event.key == pygame.K_F2:
                    Settings.SOUNDFLAG = not Settings.SOUNDFLAG
                elif event.key == pygame.K_w:
                    if not Settings.KI["left"]:
                        self._paddle["left"].update(action="up")
                elif event.key == pygame.K_s:
                    if not Settings.KI["left"]:
                        self._paddle["left"].update(action="down")
                elif event.key == pygame.K_1:
                    Settings.KI["left"] = not Settings.KI["left"]
                    if not Settings.KI["left"]:
                        self._paddle["left"].update(action="halt")
                elif event.key == pygame.K_2:
                    Settings.KI["right"] = not Settings.KI["right"]
                    if not Settings.KI["right"]:
                        self._paddle["right"].update(action="halt")
                elif event.key == pygame.K_p:
                    if not self._helping:
                        self._pausing = not self._pausing  # Toogle Pausenmodus§\label{srcPong0805}§
                elif event.key == pygame.K_h:
                    if not self._pausing:
                        self._helping = not self._helping  # Toogle Hilfemodus§\label{srcPong0806}§
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if not Settings.KI["right"]:
                        self._paddle["right"].update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    if not Settings.KI["left"]:
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

    def _paddlecontroler(self, paddle: pygame.sprite.Sprite) -> None:
        if paddle.rect.centery > self._ball.rect.centery and paddle.rect.top > 10:
            paddle.update(action="up")
        elif paddle.rect.centery < self._ball.rect.centery and paddle.rect.bottom < Settings.WINDOW.bottom - 10:
            paddle.update(action="down")
        else:
            paddle.update(action="halt")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
