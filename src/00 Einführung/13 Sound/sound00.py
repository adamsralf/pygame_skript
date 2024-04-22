import os
from time import time
from typing import Any, Tuple

import pygame
from pygame.constants import (
    K_ESCAPE,
    K_MINUS,
    K_PLUS,
    KEYDOWN,
    KEYUP,
    QUIT,
    K_f,
    K_j,
    K_p,
)


class Settings:
    WINDOW: pygame.rect.Rect = pygame.rect.Rect(
        0, 0, 600, 800
    )  # Rect §\label{srcSound0001}§
    FPS = 60
    PATH: dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")
    START_DISTANCE = 20

    @staticmethod
    def get_file(filename: str) -> str:
        return os.path.join(Settings.PATH["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        return os.path.join(Settings.PATH["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        return os.path.join(Settings.PATH["sound"], filename)


class Game:
    def __init__(self) -> None:
        pygame.init()  # Auch mixer §\label{srcSound0002}§
        self.screen = pygame.display.set_mode(Settings.WINDOW.size)
        pygame.display.set_caption('Fingerübung "Sound"')
        self.clock = pygame.time.Clock()
        self.font_bigsize = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.running = True
        self.pause = False
        self.volume: float = 0.1  # Lautstärke §\label{srcSound0003}§
        self.sounds()

    def sounds(self) -> None:
        pygame.mixer.music.load(Settings.get_sound("Lucifer.mid"))
        pygame.mixer.music.set_volume(self.volume)  # Lautstärke §\label{srcSound0004}§
        pygame.mixer.music.play(-1, 0.0)  # Endlos abspielen §\label{srcSound0005}§
        self.bubble: pygame.mixer.Sound = pygame.mixer.Sound(
            Settings.get_sound("plopp1.mp3")
        )  # §\label{srcSound0006}§
        self.clash: pygame.mixer.Sound = pygame.mixer.Sound(
            Settings.get_sound("glas.wav")
        )

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == KEYUP:
                if event.key == K_f:
                    self.music_start_stop(fadeout=5000)
                elif event.key == K_j:
                    self.music_start_stop(loop=-1)
                elif event.key == K_p:
                    self.pause_alter()
                elif event.key == K_PLUS:
                    self.volume_alter(0.05)
                elif event.key == K_MINUS:
                    self.volume_alter(-0.05)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left
                    self.sound_play(bubble=True)
                elif event.button == 3:  # right
                    self.sound_play(clash=True)
                elif event.button == 4:  # up
                    self.volume_alter(0.05)
                elif event.button == 5:  # down
                    self.volume_alter(-0.05)

    def sound_play(self, **kwargs: Any) -> None:
        if "bubble" in kwargs.keys():
            self.bubble.play()
        if "clash" in kwargs.keys():
            self.clash.play()

    def music_start_stop(self, **kwargs: Any) -> None:
        if "fadeout" in kwargs.keys():
            pygame.mixer.music.fadeout(kwargs["fadeout"])
        if "loop" in kwargs.keys():
            pygame.mixer.music.play(kwargs["loop"], 0.0)

    def pause_alter(self) -> None:
        if self.pause:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.pause = not self.pause  # §\label{srcSound0007}§

    def volume_alter(self, delta: float) -> None:
        self.volume += delta
        if self.volume > 1.0:
            self.volume = 1.0
        elif self.volume < 0.0:
            self.volume = 0.0
        pygame.mixer.music.set_volume(self.volume)

    def draw(self) -> None:
        self.screen.fill("black")

        volume = self.font_bigsize.render(
            f"Lautstärke: {self.volume:3.2f}", True, "red"
        )
        rect = volume.get_rect()
        rect.center = Settings.WINDOW.center
        self.screen.blit(volume, rect)

        pygame.display.flip()

    def update(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
        pygame.quit()


def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 30"
    Game().run()


if __name__ == "__main__":
    main()
