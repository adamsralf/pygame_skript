import os
from typing import Tuple

import pygame
from pygame.constants import (K_ESCAPE, K_KP_MINUS, K_KP_PLUS, K_MINUS, K_PLUS,
                              KEYDOWN, KMOD_SHIFT, QUIT, K_b, K_g, K_r)


class Settings:
    WINDOW = pygame.rect.Rect((0, 0), (700, 300))
    FPS = 60


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, fontsize: int, fontcolor: list[int], center: Tuple[int, int], text: str = 'Hello World!') -> None:
        super().__init__()
        self.image = None
        self.rect = None
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fontsize_update(0)                     # 0! §\label{srcTextoutputSimple02}§
        self.text = text
        self.center = center
        self.render()                               # Alle Infos zusammen §\label{srcTextoutputSimple03}§

    def render(self) -> None:
        self.image = self.font.render(self.text, True, self.fontcolor)  # Bitmap §\label{srcTextoutputSimple04}§
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def fontsize_update(self, step: int = 1) -> None:
        self.fontsize += step
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)  # §\label{srcTextoutputSimple01}§

    def fontcolor_update(self, delta: Tuple[int, int, int]) -> None:
        for i in range(3):
            self.fontcolor[i] = (self.fontcolor[i] + delta[i]) % 256

    def update(self) -> None:
        self.render()


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 150"
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(Settings.WINDOW.size)
    pygame.display.set_caption("Textausgabe mit Fonts")

    hello = TextSprite(24, [255, 255, 255], (Settings.WINDOW.center))  # Gruß§\label{srcTextoutputSimple07}§
    info = TextSprite(12, [255, 0, 0], (Settings.WINDOW.centerx, Settings.WINDOW.bottom-20))      # Fontinfo§\label{srcTextoutputSimple08}§
    all_sprites = pygame.sprite.Group()
    all_sprites.add(hello, info)

    running = True
    while running:
        clock.tick(Settings.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_KP_PLUS or event.key == K_PLUS:     # Größer §\label{srcTextoutputSimple05}§
                    hello.fontsize_update(+1)
                elif event.key == K_KP_MINUS or event.key == K_MINUS:   # Kleiner §\label{srcTextoutputSimple06}§
                    hello.fontsize_update(-1)
                elif event.key == K_r:
                    if event.mod & KMOD_SHIFT:
                        hello.fontcolor_update((-1, 0, 0))              # Weniger Rot§\label{srcTextoutputSimple09}§
                    else:
                        hello.fontcolor_update((+1, 0, 0))              # Mehr Rot§\label{srcTextoutputSimple10}§
                elif event.key == K_g:
                    if event.mod & KMOD_SHIFT:
                        hello.fontcolor_update((0, -1, 0))              # Weniger Grün
                    else:
                        hello.fontcolor_update((0, +1, 0))              # Mehr Grün
                elif event.key == K_b:
                    if event.mod & KMOD_SHIFT:
                        hello.fontcolor_update((0, 0, -1))              # Weniger Blau
                    else:
                        hello.fontcolor_update((0, 0, +1))              # Mehr Blau

        info.text = f"size={hello.fontsize}, r={hello.fontcolor[0]}, g={hello.fontcolor[1]}, b={hello.fontcolor[2]}"
        all_sprites.update()
        screen.fill((200, 200, 200))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
