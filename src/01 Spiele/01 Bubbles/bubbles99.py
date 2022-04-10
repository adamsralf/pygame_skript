"""A simple desktop game implemented with Pygame.

Credits:
 * Fishtank image: https://www.pngwing.com/en/free-png-vadpk
 * Sound: https://www.fesliyanstudios.com/royalty-free-sound-effects-download
"""
import os
from math import sqrt
from random import randint
from time import time
from typing import Any, Dict, Tuple

import pygame
from pygame.constants import (K_ESCAPE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN,
                              MOUSEBUTTONUP, QUIT, K_j, K_n, K_p)


class BubbleContainer:
    """A simple container class to manage the bubbles of different sizes."""

    def __init__(self, filename: str) -> None:
        """Constructor.

        Args:
            filename (str): Filename of the bubble picture file
        """
        imagename = Game.get_image(filename)
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Game.radius["min"], Game.radius["max"] + 1)
        }

    def get(self, radius: int) -> pygame.surface.Surface:
        """Gets the bubble image with the radius <radius>.

        Args:
            radius (int): radius of the bubble

        Returns:
            pygame.surface.Surface: Scaled image of the bubble
        """
        radius = max(Game.radius["min"], radius)
        radius = min(Game.radius["max"], radius)
        return self._images[radius]


class Timer:
    """Timer in order to check time periodes."""

    def __init__(self, duration: int, with_start: bool = True) -> None:
        """Constructor

        Args:
            duration (int): duration of the time interval in milli seconds
            with_start (bool, optional): Controls if the first period will count (True) or not (False). Defaults to True.
        """
        self.duration = duration
        if with_start:
            self._next = pygame.time.get_ticks()
        else:
            self._next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        """Checks if the end of a time period is reached or exceeded.

        Returns:
            bool: True if the end of the period is reached or exceeded; otherwise False
        """
        if pygame.time.get_ticks() > self._next:
            self._next = pygame.time.get_ticks() + self.duration
            return True
        return False


class Background:
    """Sprite class with nearly no function for drawing the background image."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()
        imagename = Game.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Game.window.size)
        self.rect = self.image.get_rect()


class Message(pygame.sprite.DirtySprite):
    """Draws a shadow and a text in the foreground of the game."""

    def __init__(self, filename: str) -> None:
        super().__init__()
        imagename = Game.get_image(filename)
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dirty = 1


class Bubble(pygame.sprite.DirtySprite):
    """The sprite class of the bubble."""

    def __init__(self, speed: int) -> None:
        """Constructor."""
        super().__init__()
        self.mode = "blue"
        self.radius = Game.radius["min"]
        self.image = Game.bubble_container[self.mode].get(self.radius)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.dirty = 1
        self.fradius = float(self.radius)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Let the bubble grow.

        Args:
            *args (Tuple[int]): not used
            **kwargs Dict[str, Any]: possible key/value pairs: 
                                      (action/grow), (action/sting), 
                                      (mode/blue), (mode/red))
        """
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Game.deltatime
                self.fradius = min(self.fradius, Game.radius["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = Game.bubble_container[self.mode].get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.dirty = 1
            elif kwargs["action"] == "sting":
                self.stung()
        elif "mode" in kwargs.keys():
            self.set_mode(kwargs["mode"])

    def set_mode(self, mode: str) -> None:
        """Sets the bubble in the mode "red" or "blue".

        Args:
            mode (str): "red" oder "blue"
        """
        if mode != self.mode:
            self.dirty = 1
            self.mode = mode
            self.image = Game.bubble_container[self.mode].get(self.radius)

    def randompos(self) -> None:
        """Computes a new position of the center by random."""
        bubbledistance = Game.distance + Game.radius["min"]
        centerx = randint(Game.playground.left + bubbledistance, Game.playground.right - bubbledistance)
        centery = randint(Game.playground.top + bubbledistance, Game.playground.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def stung(self):
        """The bubble removes itself and the score increases."""
        self.kill()
        Game.points += self.radius


class Points(pygame.sprite.DirtySprite):
    """Class in order to generate a image of the score."""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.oldpoints = -1
        self.dirty = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Let the bubble grow.

        Args:
            *args (Tuple[int]): not used
            **kwargs Dict[str, Any]: not used
        """
        if self.oldpoints != Game.points:
            self.image = self._font.render(f"Points: {Game.points}", True, "red")
            self.rect = self.image.get_rect()
            self.rect.left = Game.box.left
            self.rect.top = Game.box.top
            self.dirty = 1


class Game:
    """The class Game is main starting class of the game."""

    window = pygame.rect.Rect(0, 0, 1220, 1002)
    fps = 60
    deltatime = 1.0/fps
    path: Dict[str, str] = {}
    path["file"] = os.path.dirname(os.path.abspath(__file__))
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")
    caption = 'Fingerübung "Bubbles"'
    radius = {"min": 15, "max": 240}
    distance = 50
    playground = pygame.rect.Rect(90, 90, 1055, 615)
    max_bubbles = playground.height * playground.width // 10000
    box = pygame.rect.Rect(90, 770, 1055, 1300)
    points = 0
    bubble_container: Dict[str, BubbleContainer] = {}
    sound_container: Dict[str, pygame.mixer.Sound] = {}

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Game.path["file"], filename)
        """Full path of the file in the main path.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename
        """

    @staticmethod
    def get_image(filename: str) -> str:
        """Full path of the image file.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename of the image file
        """
        return os.path.join(Game.path["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        """Full path of the sound file.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename of the sound file
        """
        return os.path.join(Game.path["sound"], filename)

    def __init__(self) -> None:
        """Constructor."""
        pygame.init()
        self._screen = pygame.display.set_mode(Game.window.size)
        pygame.display.set_caption(Game.caption)
        self._clock = pygame.time.Clock()
        Game.bubble_container["blue"] = BubbleContainer("blase1.png")
        Game.bubble_container["red"] = BubbleContainer("blase2.png")
        Game.sound_container["bubble"] = pygame.mixer.Sound(Game.get_sound("plopp1.mp3"))
        Game.sound_container["burst"] = pygame.mixer.Sound(Game.get_sound("burst.mp3"))
        Game.sound_container["clash"] = pygame.mixer.Sound(Game.get_sound("glas.wav"))
        self._background = Background()
        self._all_sprites = pygame.sprite.LayeredDirty()
        self._all_sprites.clear(self._screen, self._background.image)
        self._all_sprites.set_timing_treshold(1000.0/Game.fps)
        self._running = True
        self._pausing = False
        self._pause = Message("pause.png")
        self._restart = Message("neustart.png")

        self.restart()

    def watch_for_events(self) -> None:
        """Looking for any type of event and poke a reaction."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
            elif event.type == KEYUP:
                if event.key == K_p:
                    self.setpause()
                elif event.key == K_j:
                    self._do_start = True
                elif event.key == K_n:
                    self._running = False
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3:
                    self.setpause()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:                           # left
                    self.sting(pygame.mouse.get_pos())

    def draw(self) -> None:
        """Draws all sprite on the screen."""
        rects = self._all_sprites.draw(self._screen)
        # pygame.draw.rect(self._screen, "red", Game.playground, 2)
        # for b in self._all_bubbles:
        #     pygame.draw.rect(self._screen, "red", b.rect, 2)  # type: ignore
        pygame.display.update(rects)  # type: ignore

    def update(self) -> None:
        """This method is responsible for the main game logic."""
        if self._do_start:
            self.restart()
        if not self._pausing and self._running:
            if self.check_bubblecollision():
                if not self._restarting:
                    Game.sound_container["clash"].play()
                    self._all_sprites.add(self._restart)
                    self._restarting = True
            else:
                self._all_sprites.update(action="grow")
                self.spawn_bubble()
            self.set_mousecursor()

    def restart(self):
        """Resets all attributes in order to start/restart the game."""
        Game.points = 0
        self._all_sprites.empty()
        self._all_sprites.add(Points())
        self._bubble_speed = 10
        self._timer_bubble = Timer(500, False)
        self._timer_bubble_speed = Timer(10000, False)
        self._do_start = False
        self._restarting = False

    def setpause(self):
        """Manages the pause mode."""
        if not self._pausing:
            self._all_sprites.add(self._pause)
        else:
            self._pause.kill()
        self._pausing = not self._pausing

    def spawn_bubble(self) -> None:
        """Spawns a new bubble and checks if there is enough space around the bubble."""
        if self._timer_bubble_speed.is_next_stop_reached():
            if self._bubble_speed < 100:
                self._bubble_speed += 5
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_sprites) <= Game.max_bubbles:
                b = Bubble(self._bubble_speed)
                tries = 100
                while tries > 0:
                    b.randompos()
                    b.radius += Game.distance
                    collided = pygame.sprite.spritecollide(b, self._all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= Game.distance
                    if collided:
                        tries -= 1
                    else:
                        self._all_sprites.add(b)
                        Game.sound_container["bubble"].play()
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        """Checks if a point is inside or on the edge of the circle.

        Args:
            point (Tuple[int, int]): Coordinates of the point
            sprite (pygame.sprite.Sprite): Sprite with self.radius attribute

        Returns:
            bool: True if the point is inside or on the edge; otherwise False
        """
        if hasattr(sprite, 'radius'):
            deltax = point[0] - sprite.rect.centerx  # type: ignore
            deltay = point[1] - sprite.rect.centery  # type: ignore
            return (sqrt(deltax * deltax + deltay * deltay) <= sprite.radius)  # type: ignore
        return False

    def set_mousecursor(self) -> None:
        """Changes the mouse cursor depending if it is inside or on the edge of a bubble."""
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self._all_sprites:
            if self.collidepoint(pos, b):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def sting(self, mousepos: Tuple[int, int]) -> None:
        """If the mouse position is inside a bubble, burst it."""
        for bubble in self._all_sprites:
            if self.collidepoint(mousepos, bubble):
                Game.sound_container["burst"].play()
                bubble.update(action="sting")

    def check_bubblecollision(self) -> bool:
        """Checks if two bubbles collide or a bubble the playground border reaches.

        Returns:
            bool: True if bubbles or a bubble collides; otherwise False
        """
        for index1 in range(0, len(self._all_sprites) - 1):
            for index2 in range(index1 + 1, len(self._all_sprites)):
                bubble1 = self._all_sprites.sprites()[index1]
                bubble2 = self._all_sprites.sprites()[index2]
                if type(bubble1).__name__ == "Bubble" and type(bubble2).__name__ == "Bubble":
                    if pygame.sprite.collide_circle(bubble1, bubble2):
                        bubble1.update(mode="red")
                        bubble2.update(mode="red")
                        return True
                    if not Game.playground.contains(bubble1):
                        bubble1.update(mode="red")
                        return True
                    if not Game.playground.contains(bubble2):
                        bubble2.update(mode="red")
                        return True
        return False

    def run(self) -> None:
        """Starting point and main loop of the game."""
        time_previous = time()
        self._running = True
        while self._running:
            self.watch_for_events()
            self.update()
            self.draw()
            self._clock.tick(Game.fps)
            time_current = time()
            Game.deltatime = time_current - time_previous
            time_previous = time_current
        # pygame.time.wait(2000)
        pygame.quit()


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
