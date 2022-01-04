import pygame §\label{srcStart01}§
import os

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50" # Fensterposition §\label{srcStart02}§
    pygame.init()                                 # Subsystem starten§\label{srcStart03}§
    pygame.display.set_caption('Mein erstes PyGame-Programm');§ \label{srcStart04}§

    screen = pygame.display.set_mode((600, 400))  # Fenstertitel§\label{srcStart05}§
    clock = pygame.time.Clock()

    running = True 
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        pygame.display.flip()

    pygame.quit()
