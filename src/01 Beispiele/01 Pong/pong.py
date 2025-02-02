"""
This module contains the implementation of the Pong game.

You can play the game by <up>/<down> and <w>/<s> keys. Press <h> for help and <p> for a pause. 

I used some resources:   
- Python documentation: https://docs.python.org/3/
- Pygame-ce documentation: https://www.pygame-ce.org/docs/
- Pong-Tutorial of freeCodeCamp.org: https://www.youtube.com/watch?v=C6jJg9Zan7w
- Pong-Tutorial of Clear Code: https://www.youtube.com/watch?v=Qf3-aDXG8q4
- Sound of the service: https://www.soundfishing.eu/sound/tennis
- Sound of the bouncing: https://pixabay.com/sound-effects/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=39028"

Versions:
- Python: 3.12.0
- Pygame-ce: 2.4.1

Classes:
- Settings: Represents the project global settings.
- MyEvents: A static class for accessing event information easily.
- Background: Represents the background sprite.
- Pause: Represents the pause sprite.
- Help: Represents the help screen.
- Paddle: Represents a paddle.
- Ball: Represents the ball.
"""

import os
from random import choice, randint
from time import time
from typing import Any, Tuple

import pygame


class Settings:
    """Project global settings."""

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
        """Returns the absolute path of a soundfile.

        Args:
            filename (str): The filename with extension.

        Returns:
            str: The absolute path of a soundfile combined with the filename.
        """
        return os.path.join(Settings.PATH["sound"], filename)


class MyEvents:
    """A static class in order to access event infos easily"""

    POINT_FOR = pygame.USEREVENT
    MYEVENT = pygame.event.Event(POINT_FOR, player=0)


class Background(pygame.sprite.Sprite):
    """A simple background sprite. Derived from pygame.sprite.Sprite.

    Attributes:
        image (pygame.Surface): The image representing the background.
        rect (pygame.Rect): The rectangle representing the position and size of the background.

    Methods:
        __init__(*groups: Tuple[pygame.sprite.Group]) -> None: Initializes the Background object.
        _paint_net() -> None: A helper method to draw the net on the background.
    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor"""
        super().__init__(*groups)
        self.image = pygame.surface.Surface(Settings.WINDOW.size).convert()
        self.rect = self.image.get_rect()
        self.image.fill("darkred")
        self._paint_net()

    def _paint_net(self) -> None:
        """A helping method to draw the net."""
        net_rect = pygame.rect.Rect(0, 0, 0, 0)
        net_rect.centerx = Settings.WINDOW.centerx
        net_rect.top = 50
        net_rect.size = (3, 30)
        while net_rect.bottom < Settings.WINDOW.bottom:
            pygame.draw.rect(self.image, "grey", net_rect, 0)
            net_rect.move_ip(0, 40)


class Pause(pygame.sprite.Sprite):
    """A simple pause sprite. Derived from pygame.sprite.Sprite.

    Attributes:
        rect (pygame.Rect): The rectangular area occupied by the pause sprite.
        image (pygame.Surface): The surface representing the pause sprite.

    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor."""
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(Settings.WINDOW.topleft, Settings.WINDOW.size)
        self.image = pygame.surface.Surface(self.rect.size).convert_alpha()
        self.image.fill([120, 120, 120, 200])  # transparentes Grau§\label{srcPong0801}§


class Help(pygame.sprite.Sprite):
    """A class representing the help screen in the Pong game. Derived from pygame.sprite.Sprite.


    Attributes:
        rect (pygame.Rect): The rectangle representing the size and position of the help screen.
        image (pygame.Surface): The surface representing the image of the help screen.

    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor."""
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(Settings.WINDOW.topleft, Settings.WINDOW.size)
        self.image = pygame.surface.Surface(self.rect.size).convert_alpha()
        self.image.fill([20, 20, 20, 200])  # transparent gray
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text_l = "h\np\nESC\n\nF2\nk\nl\nr\n\nUP\nDOWN\nw\ns"
        text_r = "- toggle help mode\n- toggle pause mode\n- quit\n\n- toggle sound mode\n"
        text_r += "- toggle both paddles AI mode\n- toggle left paddle AI mode\n- toggle right paddle AI mode\n\n"
        text_r += "- move left paddle up\n- move left paddle down\n- move right paddle up\n- move right paddle down"
        lines = font.render(text_l, True, "white")
        self.image.blit(lines, (10, 10))
        lines = font.render(text_r, True, "white")
        self.image.blit(lines, (10 + 70, 10))


class Paddle(pygame.sprite.Sprite):
    """Represents a paddle in the Pong game.

    Attributes:
        BORDERDISTANCE (dict): A dictionary containing the horizontal and vertical distance of the paddle from the border.
        DIRECTION (dict): A dictionary containing the possible directions of the paddle.
    """

    BORDERDISTANCE = {"horizontal": 50, "vertical": 10}
    DIRECTION = {"up": -1, "down": 1, "halt": 0}

    def __init__(self, player: str, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor

        Args:
            player (str): The player of the paddle ("left" or "right").
            *groups (Tuple[pygame.sprite.Group]): Optional sprite groups to add the paddle to.
        """
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
        """Computes the new status of the paddle.

        Args:
            action(str): "move" computes the new position.
                            "up" sets the direction to up.
                            "down" sets the direction to down.
                            "halt" stops the paddle.

        Returns:
            None
        """
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self._move()
            elif kwargs["action"] in Paddle.DIRECTION.keys():
                self._direction = Paddle.DIRECTION[kwargs["action"]]
        self._select_image()
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        """Computes the new position of the paddle.

        Returns:
            None
        """
        if self._direction != Paddle.DIRECTION["halt"]:
            self.rect.move_ip(0, self._speed * self._direction * Settings.DELTATIME)
            if self._direction == Paddle.DIRECTION["up"]:
                self.rect.top = max(self.rect.top, Paddle.BORDERDISTANCE["vertical"])
            elif self._direction == Paddle.DIRECTION["down"]:
                self.rect.bottom = min(self.rect.bottom, Settings.WINDOW.height - Paddle.BORDERDISTANCE["vertical"])

    def _select_image(self) -> None:
        """Selects the image for the paddle based on the player and KI mode.

        Returns:
            None
        """
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
    """A class representing the ball in the Pong game.Derived from pygame.sprite.Sprite.

    Attributes:
        rect (pygame.Rect): The rectangular area occupied by the ball.
        image (pygame.Surface): The surface representing the ball.
        _speed (int): The speed of the ball.
        _speedxy (pygame.Vector2): The velocity of the ball in both x and y directions.
        _sounds (dict): A dictionary containing the sounds used by the ball.
        _channel (pygame.mixer.Channel): The audio channel used to play the sounds.

    Methods:
        __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
            Initializes a new instance of the Ball class.
        update(self, *args: Any, **kwargs: Any) -> None:
            Updates the ball's position and status.
        _move(self) -> None:
            Computes the new position or triggers a new service.
        _service(self) -> None:
            Sets the position to the center of the window and throws the ball in a random direction.
        _horizontal_flip(self) -> None:
            Toggles the direction from left to right or vice versa.
        _vertical_flip(self) -> None:
            Toggles the direction from up to down or vice versa.
        _respeed(self) -> None:
            Computes a new and faster speed.
    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        """Constructor."""
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
        """Computes the new status.

        Returns:
            action (str): "move" -> new position
                            "hflip" -> toggles the horizontal direction
                            "vflip" -> toggles the vertical direction
                            "reset" -> new service of player left or right
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
        return super().update(*args, **kwargs)

    def _move(self) -> None:
        """Computes the new position or triggers a new service."""
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
        """Sets the position to the center of the window and throws the ball in a random direction."""
        self.rect.center = Settings.WINDOW.center
        self._speedxy = pygame.Vector2(choice([-1, 1]), choice([-1, 1])) * self._speed

    def _horizontal_flip(self) -> None:
        """Toggles the direction from left to right vice versa."""
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
        """Toggles the direction from up to down vice versa."""
        if Settings.SOUNDFLAG:
            rel_pos = self.rect.centerx / Settings.WINDOW.width
            self._channel.set_volume(1.0 - rel_pos, rel_pos)
            self._channel.play(self._sounds["bounce"])
        self._speedxy.y *= -1

    def _respeed(self) -> None:
        """Computes a new and faster speed."""
        self._speedxy.x += randint(0, self._speed // 4)
        self._speedxy.y += randint(0, self._speed // 4)


class Score(pygame.sprite.Sprite):
    """A class representing the score in a Pong game. Derived from pygame.sprite.Sprite.

    Attributes:
        _font (pygame.font.Font): The font used for rendering the score.
        _score (dict): A dictionary storing the scores of the players.
        image (pygame.surface.Surface): The rendered image of the score.
        rect (pygame.rect.Rect): The rectangle representing the position and size of the score image.
    """

    def __init__(self, *groups: Tuple[pygame.sprite.Group]):
        """Constructor method for the Score class.

        Args:
            *groups (Tuple[pygame.sprite.Group]): The groups to which the Score sprite should be added.
        """
        super().__init__(*groups)
        self._font = pygame.font.SysFont(None, 30)
        self._score = {1: 0, 2: 0}
        self.image: pygame.surface.Surface = None
        self.rect: pygame.rect.Rect = None
        self._render()

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Increases the score of the player and rerenders the sprite.

        Args:
            player(str) : "left" or "right".
        """
        if "player" in kwargs.keys():
            self._score[kwargs["player"]] += 1
            self._render()
        return super().update(*args, **kwargs)

    def _render(self):
        """Renders the score."""
        self.image = self._font.render(f"{self._score[1]} : {self._score[2]}", True, "white")
        self.rect = self.image.get_rect(centerx=Settings.WINDOW.centerx, top=15)


class Game:
    """Represents a game of Pong.

    Attributes:
        _window (pygame.Window): The game Window.
        _screen (pygame.Surface): The game surface.
        _clock (pygame.time.Clock): The game clock.
        _background (pygame.sprite.GroupSingle): The background sprite group.
        _all_sprites (pygame.sprite.Group): The group containing all moving game sprites.
        _paddle (dict): A dictionary containing the left and right paddles.
        _ball (Ball): The game ball.
        _score (Score): The game score.
        _running (bool): Flag indicating if the game is running.
        _pausing (bool): Flag indicating if the game is paused.
        _helping (bool): Flag indicating if the help screen is displayed.
        _pause (pygame.sprite.GroupSingle): The pause screen sprite group.
        _help (pygame.sprite.GroupSingle): The help screen sprite group.
    """

    def __init__(self):
        """
        Initializes the Pong game.

        This method initializes the game window, sets the caption, creates game objects,
        and sets the initial game state variables.

        Parameters:
            None

        Returns:
            None
        """
        pygame.init()
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
        self._pausing = False
        self._helping = False
        self._pause = pygame.sprite.GroupSingle(Pause())
        self._help = pygame.sprite.GroupSingle(Help())

    def run(self):
        """Starts the game loop and runs the game."""
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
        """Updates the game state."""
        if not (self._pausing or self._helping):
            self._check_collision()
            for i in Settings.KI.keys():
                if Settings.KI[i]:
                    self._paddlecontroler(self._paddle[i])
            self._all_sprites.update(action="move")

    def draw(self):
        """Draws the game on the screen."""
        self._background.draw(self._screen)
        self._all_sprites.draw(self._screen)
        if self._pausing:
            self._pause.draw(self._screen)
        elif self._helping:
            self._help.draw(self._screen)
        self._window.flip()

    def watch_for_events(self):
        """Watches for game events and handles them."""
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
                        self._pausing = not self._pausing
                elif event.key == pygame.K_h:
                    if not self._pausing:
                        self._helping = not self._helping
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
        """Checks for collision between the ball and paddles."""
        if pygame.sprite.collide_rect(self._ball, self._paddle["left"]):
            self._ball.update(action="hflip")
            self._ball.rect.left = self._paddle["left"].rect.right + 1
        elif pygame.sprite.collide_rect(self._ball, self._paddle["right"]):
            self._ball.update(action="hflip")
            self._ball.rect.right = self._paddle["right"].rect.left - 1

    def _paddlecontroler(self, paddle: pygame.sprite.Sprite) -> None:
        """Controls the movement of a paddle based on the ball's position.

        Args:
            paddle (pygame.sprite.Sprite): The paddle to control.
        """
        if paddle.rect.centery > self._ball.rect.centery and paddle.rect.top > 10:
            paddle.update(action="up")
        elif paddle.rect.centery < self._ball.rect.centery and paddle.rect.bottom < Settings.WINDOW.bottom - 10:
            paddle.update(action="down")
        else:
            paddle.update(action="halt")


def main():
    Game().run()


if __name__ == "__main__":
    main()
