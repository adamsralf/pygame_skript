import os
from typing import Tuple

import pygame


class Settings:
    WINDOW = pygame.rect.Rect(0, 0, 1000, 800)
    FPS = 30
    PATH: dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")
    #size = 5
    #number = 100
    #size = 5
    #number = 4000
    #size = 30
    #number = 100
    #size = 50
    #number = 100
    size = 100
    number = 40

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.PATH["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.PATH["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.PATH["sound"], filename)
