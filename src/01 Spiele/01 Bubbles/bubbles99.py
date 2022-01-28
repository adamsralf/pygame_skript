"""A simple desktop game implemented with Pygame.

Credits:
 * Fishtank image: https://www.pngwing.com/en/free-png-vadpk
 * Sound: https://www.fesliyanstudios.com/royalty-free-sound-effects-download
"""
import os
from math import sqrt
from random import randint
from typing import Any, Dict, Tuple

import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, KEYUP, QUIT, K_j, K_n, K_p


class Settings:
    """Global Settings of the project."""

    window = {"width": 1220, "height": 1002}
    fps = 60
    path: Dict[str, str] = {"file": os.path.dirname(os.path.abspath(__file__))}
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")
    caption = 'Fingerübung "Bubbles"'
    radius = {"min": 15, "max": 240}
    distance = 50
    playground = pygame.Rect(90, 90, 1055, 615)
    max_bubbles = playground.height * playground.width // 10000
    box = pygame.Rect(90, 770, 1055, 1300)
    points = 0
    bubble_container: Dict[str, Any] = {}

    @staticmethod
    def get_dim() -> Tuple[int, int]:
        """Dimensions of the screen.
        Returns:
            (int, int): Width and height of the window.
        """
        return (Settings.window["width"], Settings.window["height"])

    @staticmethod
    def get_image(filename: str) -> str:
        """Full path of the image file.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename of the image file
        """
        return os.path.join(Settings.path["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        """Full path of the sound file.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename of the sound file
        """
        return os.path.join(Settings.path["sound"], filename)


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


class Background(pygame.sprite.Sprite):
    """Sprite class with nearly no function for drawing the background image."""

    def __init__(self, filename: str = "aquarium.png") -> None:
        """Constructor.

        Args:
            filename (str, optional): Filename of the background image. Defaults to "aquarium.png".
        """
        super().__init__()
        self.image = pygame.image.load(Settings.get_image(filename)).convert()
        self.image = pygame.transform.scale(self.image, Settings.get_dim())
        self.rect = self.image.get_rect()


class Foreground:
    """Draws a shadow and a text in the foreground of the game."""

    def __init__(self, message: str) -> None:
        """Constructor.
        Args:
            message (str): Message to be displayed.
        """
        super().__init__()
        self._image = pygame.image.load(Settings.get_image("hintergrund.png")).convert_alpha()
        self._image = pygame.transform.scale(self._image, Settings.get_dim())
        self._image.set_alpha(150)
        self._rect_image = self._image.get_rect()
        font_bigsize = pygame.font.Font(pygame.font.get_default_font(), 40)
        self._text = font_bigsize.render(message, True, (255, 0, 0))
        self._rect_text = self._text.get_rect()
        self._rect_text.centerx = Settings.window["width"] // 2
        self._rect_text.centery = Settings.window["height"] // 2 - 50

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draws the shadow over the hole screen and the message in the center of the screen.

        Args:
            screen (pygame.surface.Surface): Usually the screen image
        """
        screen.blit(self._image, self._rect_image)
        screen.blit(self._text, self._rect_text)


class SoundContainer:
    """A simple container class to manage the sound clips."""

    def __init__(self) -> None:
        """Constructor."""
        self._sounds: Dict[str, pygame.mixer.Sound] = {"bubble": pygame.mixer.Sound(Settings.get_sound("plopp1.mp3"))}
        self._sounds["burst"] = pygame.mixer.Sound(Settings.get_sound("burst.mp3"))
        self._sounds["clash"] = pygame.mixer.Sound(Settings.get_sound("glas.wav"))

    def get(self, effect: str) -> pygame.mixer.Sound:
        """Gets the sound clip with the key <effect>.

        Args:
            effect (str): Key of the sound effect

        Returns:
            pygame.mixer.Sound: Sound clip
        """
        return self._sounds[effect]


class BubbleContainer:
    """A simple container class to manage the bubbles of different sizes."""

    def __init__(self, filename: str) -> None:
        """Constructor

        Args:
            filename (str): Filename of the bubble picture file
        """
        image = pygame.image.load(Settings.get_image(filename)).convert_alpha()
        self._images: Dict[int, pygame.surface.Surface] = {
            i: pygame.transform.scale(image, (i * 2, i * 2))
            for i in range(Settings.radius["min"], Settings.radius["max"] + 1)
        }

    def get(self, radius: int) -> pygame.surface.Surface:
        """Gets the bubble image with the radius <radius>.

        Args:
            radius (int): radius of the bubble

        Returns:
            pygame.surface.Surface: Scaled image of the bubble
        """
        radius = max(Settings.radius["min"], radius)
        radius = min(Settings.radius["max"], radius)
        return self._images[radius]


class Bubble(pygame.sprite.Sprite):
    """The sprite class of the bubble."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()
        self.mode = "blue"
        self.radius = Settings.radius["min"]
        self.image = Settings.bubble_container[self.mode].get(self.radius)
        self.rect: pygame.Rect = self.image.get_rect()
        self._timer_growth = Timer(100, False)

    def update(self, *args: Tuple[int], **kwargs: Dict[str, Any]) -> None:
        """Let the bubble grow.

        Args:
            *args (Tuple[int]): not used
            **kwargs Dict[str, Any]: not used
        """
        if self._timer_growth.is_next_stop_reached():
            self.radius = min(self.radius + 1, Settings.radius["max"])
            center = self.rect.center
            self.image = Settings.bubble_container[self.mode].get(self.radius)
            self.rect = self.image.get_rect()
            self.rect.center = center

    def set_mode(self, mode: str) -> None:
        """Sets the bubble in the mode "red" or "blue".

        Args:
            mode (str): "red" oder "blue"
        """
        self.mode = mode
        self.image = Settings.bubble_container[self.mode].get(self.radius)

    def randompos(self) -> None:
        """Computes a new position of the center by random."""
        bubbledistance = Settings.distance + Settings.radius["min"]
        centerx = randint(
            Settings.playground.left + bubbledistance,
            Settings.playground.right - bubbledistance,
        )
        centery = randint(
            Settings.playground.top + bubbledistance,
            Settings.playground.bottom - bubbledistance,
        )
        self.rect.center = (centerx, centery)

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """Checks if a point is inside or on the edge of the circle.

        Args:
            point (Tuple[int, int]): Coordinates of the point

        Returns:
            bool: True if the point is inside or on the edge; otherwise False
        """
        deltax = point[0] - self.rect.centerx
        deltay = point[1] - self.rect.centery
        return sqrt(deltax * deltax + deltay * deltay) <= self.radius

    def stung(self):
        """The bubble removes itself and the score increases."""
        self.kill()
        Settings.points += self.radius


class Points(pygame.sprite.Sprite):
    """Class in order to generate a image of the score."""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        self._font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.image: pygame.surface.Surface
        self.rect: pygame.rect.Rect

    def update(self, *args: Tuple[int], **kwargs: Dict[str, Any]) -> None:
        """Let the bubble grow.

        Args:
            *args (Tuple[int]): not used
            **kwargs Dict[str, Any]: not used
        """
        self.image = self._font.render(f"Points: {Settings.points}", True, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = Settings.box.topleft


class Game:
    """The class Game is main starting class of the game."""

    def __init__(self) -> None:
        """Constructor"""
        pygame.init()
        self._sounds = SoundContainer()
        self._screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.caption)
        self._clock = pygame.time.Clock()
        Settings.bubble_container["blue"] = BubbleContainer("blase1.png")
        Settings.bubble_container["red"] = BubbleContainer("blase2.png")
        self._background = pygame.sprite.GroupSingle(Background())
        self._points = pygame.sprite.GroupSingle(Points())
        self._timer_bubble = Timer(1000, False)
        self._timer_bubble_duration = Timer(10000, False)
        self._all_bubbles = pygame.sprite.Group()
        self._running = True
        self._pause = Foreground("PAUSE")
        self._pausing = False
        self._restart = Foreground("Neustart (J/N)?")
        self._restarting = False
        self._do_start = False

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
                    self._pausing = not self._pausing
                elif event.key == K_j:
                    self._do_start = True
                elif event.key == K_n:
                    self._running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.sting(pygame.mouse.get_pos())
                elif event.button == 3:
                    self._pausing = not self._pausing

    def draw(self) -> None:
        """Draws all sprite on the screen."""
        self._background.draw(self._screen)
        self._all_bubbles.draw(self._screen)
        self._points.draw(self._screen)
        # pygame.draw.rect(self._screen, (255, 0, 0), Settings.playground, 2)
        # for b in self._all_bubbles:
        #     pygame.draw.rect(self._screen, (255, 0, 0), b.rect, 2)
        if self._pausing:
            self._pause.draw(self._screen)
        elif self._restarting:
            self._restart.draw(self._screen)
        pygame.display.flip()

    def update(self) -> None:
        """This method is responsible for the main game logic."""
        if self._do_start:
            Settings.points = 0
            self._all_bubbles.empty()
            self._timer_bubble = Timer(1000, False)
            self._timer_bubble_duration = Timer(10000, False)
            self._do_start = False
            self._restarting = False
        if not self._pausing and self._running:
            if self.check_bubblecollision():
                if not self._restarting:
                    self._sounds.get("clash").play()
                self._restarting = True
            else:
                self._all_bubbles.update()
                self._points.update()
                self.spawn_bubble()
            self.set_mousecursor()

    def spawn_bubble(self) -> None:
        """Spawns a new bubble and checks if there is enough space around the bubble."""
        if self._timer_bubble_duration.is_next_stop_reached():
            self._timer_bubble.duration = max(self._timer_bubble.duration - 100, 400)
        if self._timer_bubble.is_next_stop_reached():
            if len(self._all_bubbles) <= Settings.max_bubbles:
                bubble = Bubble()
                tries = 100
                while tries > 0:
                    bubble.randompos()
                    bubble.radius += Settings.distance
                    collided = pygame.sprite.spritecollide(bubble, self._all_bubbles, False, pygame.sprite.collide_circle)
                    bubble.radius -= Settings.distance
                    if collided:
                        tries -= 1
                    else:
                        self._all_bubbles.add(bubble)
                        self._sounds.get("bubble").play()
                        break

    def set_mousecursor(self) -> None:
        """Changes the mouse cursor depending if it is inside or on the edge of a bubble."""
        is_over = False
        pos = pygame.mouse.get_pos()
        for bubble in self._all_bubbles:
            if bubble.collidepoint(pos):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def sting(self, mousepos: Tuple[int, int]) -> None:
        """If the mouse position is inside a bubble, burst it."""
        for bubble in self._all_bubbles:
            if bubble.collidepoint(mousepos):
                self._sounds.get("burst").play()
                bubble.stung()

    def check_bubblecollision(self) -> bool:
        """Checks if two bubbles collide or a bubble the playground border reaches.

        Returns:
            bool: True if bubbles or a bubble collides; otherwise False
        """
        for index1 in range(0, len(self._all_bubbles) - 1):
            for index2 in range(index1 + 1, len(self._all_bubbles)):
                bubble1 = self._all_bubbles.sprites()[index1]
                bubble2 = self._all_bubbles.sprites()[index2]
                if pygame.sprite.collide_circle(bubble1, bubble2):
                    bubble1.set_mode("red")
                    bubble2.set_mode("red")
                    return True
                if not Settings.playground.contains(bubble1):
                    bubble1.set_mode("red")
                    return True
                if not Settings.playground.contains(bubble2):
                    bubble2.set_mode("red")
                    return True
        return False

    def run(self) -> None:
        """Starting point and main loop of the game."""
        self._running = True
        while self._running:
            self._clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        # pygame.time.wait(2000)
        pygame.quit()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    game = Game()
    game.run()
