import os
from typing import Tuple

import pygame


class Settings:
    window: pygame.rect.Rect = pygame.rect.Rect(0, 0, 1000, 800)
    fps = 60
    path: dict[str, str] = {}
    path["file"] = os.path.dirname(os.path.abspath(__file__))
    path["image"] = os.path.join(path["file"], "images")
    path["sound"] = os.path.join(path["file"], "sounds")
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
    def get_dim() -> Tuple[int, int]:
        return (Settings.window.width, Settings.window.height)

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.path["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.path["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.path["sound"], filename)
