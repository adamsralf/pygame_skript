import os
from random import randint

import pygame


class Circle:                               # Nicht wirklich nötig, aber hilfreich§\label{srcCircles0101}§
    def __init__(self, pos) -> None:
        self.posx = pos[0]
        self.posy = pos[1]
        self.radius = 20
        self.color = "blue"

    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)


def main():
    size = (300, 600)                       # Bildschirmgröße§\label{srcCircles0102}§
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()
    pygame.display.set_caption('Partikelschwarm')
    screen = pygame.display.set_mode(size)  # §\label{srcCircles0103}§
    clock = pygame.time.Clock()
    circles = []                            # Kontainer für die Kreise§\label{srcCircles0104}§

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:   # Linke Maustaste?§\label{srcCircles0105}§
            circles.append(Circle(pygame.mouse.get_pos()))

        screen.fill("white")
        for p in circles:
            p.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
