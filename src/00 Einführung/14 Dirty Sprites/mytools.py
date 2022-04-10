import json

import pygame


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


class Animation(object):
    def __init__(self, spritelist: list[pygame.surface.Surface], endless: bool, animationtime: int, colorkey: None | str | list[int] = None) -> None:
        self.images = spritelist
        self.endless = endless
        self.timer = Timer(animationtime)
        self.imageindex = -1

    def next(self) -> pygame.surface.Surface:
        if self.timer.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                if self.endless:
                    self.imageindex = 0
                else:
                    self.imageindex = len(self.images) - 1
        return self.images[self.imageindex]

    def is_ended(self) -> bool:
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False


class SpriteContainer:
    def __init__(self, rectfile: str, spritesheetfile: str, colorkey: None | str | list[int] = None) -> None:
        self._spritesheed = pygame.image.load(spritesheetfile).convert()
        if colorkey == None:
            self._spritesheed = self._spritesheed.convert_alpha()
        else:
            self._spritesheed = self._spritesheed.convert()
            self._spritesheed.set_colorkey(colorkey)
        self._rects: dict[str, dict[int, pygame.Rect]] = {}
        self._sprites: dict[str, dict[int, pygame.surface.Surface]] = {}
        self._load(rectfile)

    def _load(self, filename: str) -> None:
        with open(filename) as infile:
            data = json.load(infile)
            for spritename in data.items():
                self._rects[spritename[0]] = {}
                self._sprites[spritename[0]] = {}
                for rectdata in spritename[1].items():
                    index = int(rectdata[0])
                    self._rects[spritename[0]][index] = pygame.Rect(rectdata[1][0], rectdata[1][1], rectdata[1][2], rectdata[1][3])
                    self._sprites[spritename[0]][index] = self._spritesheed.subsurface(self._rects[spritename[0]][index])

    def get_sprites(self, key: str) -> dict[int, pygame.surface.Surface]:
        return self._sprites[key]

    def get_sprite(self, key: str, index: int = 0) -> pygame.surface.Surface:
        return self._sprites[key][index]
