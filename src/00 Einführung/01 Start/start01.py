import os

import pygame


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()
    pygame.display.set_caption('Mein erstes Pygame-Programm')

    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()                   # Clock-Objekt§\label{srcStart0101}§

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 255, 0))
        pygame.display.flip()
        clock.tick(60)                            # Taktung auf 60 fps§\label{srcStart0102}§

    pygame.quit()


if __name__ == '__main__':
    main()
