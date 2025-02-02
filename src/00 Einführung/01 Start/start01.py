import pygame


def main():
    pygame.init()
    window = pygame.Window( size=(600, 400),        
                            title = "Mein erstes Pygame-Programm", # per Übergabeparameter
                            position = (10, 50))         
    screen = window.get_surface()                   

    clock = pygame.time.Clock()                     # Clock-Objekt§\label{srcStart0101}§

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 255, 0))
        window.flip()
        clock.tick(60)                              # Taktung auf 60 fps§\label{srcStart0102}§

    pygame.quit()


if __name__ == '__main__':
    main()
