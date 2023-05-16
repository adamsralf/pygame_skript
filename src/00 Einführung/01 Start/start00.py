import os

import pygame  # Pygame-Modul (auch bei Pygame-ce!)§\label{srcStart0001}§


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50" # Fensterposition §\label{srcStart0002}§
    pygame.init()                                 # Subsystem starten§\label{srcStart0003}§
    pygame.display.set_caption('Mein erstes Pygame-Programm')  # Fenstertitel §\label{srcStart0004}§

    screen = pygame.display.set_mode((600, 400))  # Fenster erzeugen §\label{srcStart0005}§
    running = True
    while running:                                # Hauptprogammschleife: start §\label{srcStart0006}§
        for event in pygame.event.get():          # Ermitteln der Events§\label{srcStart0007}§
            if event.type == pygame.QUIT:         # Fenster X angeklickt? §\label{srcStart0008}§
                running = False
        screen.fill((0, 255, 0))                  # Spielfläche einfärben §\label{srcStart0009}§
        pygame.display.flip()                     # Doublebuffer austauschen §\label{srcStart0010}§

    pygame.quit()                                 # Subsystem beenden§\label{srcStart0011}§


if __name__ == '__main__':
    main()
