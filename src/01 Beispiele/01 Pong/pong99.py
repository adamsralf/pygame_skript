"""A simple pong clone implemented with Pygame.
"""
from random import choice
from time import time
from typing import Any, Tuple

import pygame


class MyEvents:
    """A simple container of event numbers and event objects. For this game a static class is sufficient. 
    """
    POINT_FOR = pygame.USEREVENT
    MYEVENT = pygame.event.Event(POINT_FOR, player=0)


class Settings:
    """Project global settings.
    """
    WINDOW: pygame.rect.Rect = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    DELTATIME = 1.0/FPS


class Background(pygame.sprite.Sprite):
    """A simple background sprite. Derived by pygame.sprite.Sprite.
    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor.
        """
        super().__init__(*groups)
        self.image = pygame.surface.Surface(Settings.WINDOW.size)
        self.image.fill("black")
        for ypos in range(2, Settings.WINDOW.bottom, 10):
            pygame.draw.line(self.image, "white", (Settings.WINDOW.centerx, ypos), (Settings.WINDOW.centerx, ypos+5), 2)
        self.rect = self.image.get_rect()


class Paddle(pygame.sprite.Sprite):
    """A paddle of the pong game. Derived by pygame.sprite.Sprite.
    """

    def __init__(self, player: str, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor.

        Args:
            player (str): "left" or "right" player.
        """
        super().__init__(*groups)
        self.rect = pygame.Rect(0, 0, 15, Settings.WINDOW.height//10)
        y = Settings.WINDOW.centery
        if player == "left":
            x = 50
        else:
            x = Settings.WINDOW.right - 50
        self.rect.center = (x, y)
        self._speed = Settings.WINDOW.height // 2
        self._direction = 0
        self.image = pygame.surface.Surface(self.rect.size)
        self.image.fill("yellow")

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Updates the position of the paddle.

        Args:
            kwargs (Any): key="action" with values 
                          "move" = changes the position
                          "up" , "down" = changes the direction
                          "halt" = stops the paddle
        """
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] == "up":
                self._direction = -1
            elif kwargs["action"] == "down":
                self._direction = 1
            elif kwargs["action"] == "halt":
                self._direction = 0
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        """Computes the new position.
        """
        self.rect.centery += self._speed * self._direction * Settings.DELTATIME
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > Settings.WINDOW.bottom:
            self.rect.bottom = Settings.WINDOW.bottom


class Ball(pygame.sprite.Sprite):
    """The ball of the pong game. Derived by pygame.sprite.Sprite.
    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor.
        """
        super().__init__(*groups)
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.image = pygame.surface.Surface(self.rect.size)
        pygame.draw.circle(self.image, "green", self.rect.center, self.rect.width//2)
        self._speed = Settings.WINDOW.width // 3
        self._service()

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Updates the position of the ball.

        Args:
            kwargs (Any): key="action" with values 
                          "move" = changes the position
                          "hflip" = changes the horizontal direction
                          "vflip" = changes the vertical direction
                          "reset" = sets the ball to start position and computes random directions
                          "respeed" = adds a random value to the speed
        """
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] == "hflip":
                self._horizontal_flip()
            elif kwargs["action"] == "vflip":
                self._vertical_flip()
            elif kwargs["action"] == "reset":
                self._service()
            elif kwargs["action"] == "respeed":
                self._respeed()
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        """Computes the new position.
        """
        self.rect.x += self._speedx * Settings.DELTATIME
        self.rect.y += self._speedy * Settings.DELTATIME
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
        """Sets the ball to start position and computes random directions.
        """
        self.rect.center = Settings.WINDOW.center
        self._speedx = choice([-1, 1]) * self._speed
        self._speedy = choice([-1, 1]) * self._speed

    def _horizontal_flip(self) -> None:
        """Changes the horizontal direction.
        """
        self._speedx *= -1

    def _vertical_flip(self) -> None:
        """Changes the vertical direction.
        """
        self._speedy *= -1

    def _respeed(self) -> None:
        """Adds a random value to the speed vectors.
        """
        self._speedx += choice((-self._speed//4, 0, self._speed//4))
        self._speedy += choice((-self._speed//4, 0, self._speed//4))


class Score(pygame.sprite.Sprite):
    """The Scorebitmap. Derived by pygame.sprite.Sprite.
    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]):
        """Constructor.
        """
        super().__init__(*groups)
        self.font = pygame.font.SysFont(None, 30)
        self.centerxy = (Settings.WINDOW.centerx, self.font.get_height()//2)
        self.image: pygame.surface.Surface = None
        self.rect: pygame.rect.Rect = None
        self.points = [0, 0]
        self._render()

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Updates the points a player and renders the new score.

        Args:
            kwargs (Any): key="player" with values 
                          1 = increments the points of player 1
                          2 = increments the points of player 2
        """
        if "player" in kwargs.keys():
            if kwargs["player"] == 1:
                self.points[0] += 1
                self._render()
            elif kwargs["player"] == 2:
                self.points[1] += 1
                self._render()
        return super().update(*args, **kwargs)

    def _render(self):
        """Renders the score bitmap.
        """
        self.image = self.font.render(f"{self.points[0]} : {self.points[1]}", True, "white")
        self.rect = self.image.get_rect(center=(self.centerxy))


class Game:
    """The Pong Game class.
    """

    def __init__(self) -> None:
        """Constructor
        """
        pygame.init()
        self._display = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption("My Kind of Pong")
        self._clock = pygame.time.Clock()
        self._background = pygame.sprite.GroupSingle(Background())
        self._all_sprites = pygame.sprite.Group()
        self._paddles = [Paddle("left", self._all_sprites), Paddle("right", self._all_sprites)]
        self._score = Score(self._all_sprites)
        self._ball = Ball(self._all_sprites)
        self._isComputerPlayer = [False, False]
        self._running = True

    def run(self) -> None:
        """Starting point and main loop.
        """
        time_previous = time()
        while self._running:
            self.update()
            self.draw()
            self._clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def update(self) -> None:
        """Computes the status of the next frame.
        """
        self.watch_for_events()
        self._check_collision()
        for i in range(2):
            if self._isComputerPlayer[i]:
                self._paddlecontroler(self._paddles[i])
        self._all_sprites.update(action="move")

    def draw(self) -> None:
        """Draws all sprites to the display.
        """
        self._background.draw(self._display)
        self._all_sprites.draw(self._display)
        pygame.display.update()

    def watch_for_events(self) -> None:
        """Handles pygame events and user events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_UP:
                    if not self._isComputerPlayer[1]:
                        self._paddles[1].update(action="up")
                elif event.key == pygame.K_DOWN:
                    if not self._isComputerPlayer[1]:
                        self._paddles[1].update(action="down")
                elif event.key == pygame.K_w:
                    if not self._isComputerPlayer[0]:
                        self._paddles[0].update(action="up")
                elif event.key == pygame.K_s:
                    if not self._isComputerPlayer[0]:
                        self._paddles[0].update(action="down")
                elif event.key == pygame.K_1:
                    self._isComputerPlayer[0] = not self._isComputerPlayer[0]
                    if not self._isComputerPlayer[0]:
                        self._paddles[0].update(action="halt")
                elif event.key == pygame.K_2:
                    self._isComputerPlayer[1] = not self._isComputerPlayer[1]
                    if not self._isComputerPlayer[1]:
                        self._paddles[1].update(action="halt")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if not self._isComputerPlayer[1]:
                        self._paddles[1].update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    if not self._isComputerPlayer[0]:
                        self._paddles[0].update(action="halt")
            elif event.type == MyEvents.POINT_FOR:
                self._score.update(player=event.player)

    def _check_collision(self):
        """Checks if one of the paddles collides with the ball and if then start corresponding actions.
        """
        if pygame.sprite.collide_rect(self._ball, self._paddles[0]):
            self._ball.update(action="hflip")
            self._ball.rect.left = self._paddles[0].rect.right + 1
        elif pygame.sprite.collide_rect(self._ball, self._paddles[1]):
            self._ball.update(action="hflip")
            self._ball.rect.right = self._paddles[1].rect.left - 1

    def _paddlecontroler(self, paddle) -> None:
        """Some kind of AI :-). 

        Controls the paddle instead of a human player. The 'strategy' is to run to the vertical ball position.

        Args:
            paddle (Paddle): Paddle that is to be controlled.
        """
        if paddle.rect.centery > self._ball.rect.centery and paddle.rect.top > self._ball.rect.height - 1:
            paddle.update(action="up")
        elif paddle.rect.centery < self._ball.rect.centery and paddle.rect.bottom < Settings.WINDOW.bottom - (self._ball.rect.height - 1):
            paddle.update(action="down")
        else:
            paddle.update(action="halt")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()