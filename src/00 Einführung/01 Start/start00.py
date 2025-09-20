import pygame  # Pygame-Modul (auch bei Pygame-ce!)§\label{srcStart0001}§


def main():
    pygame.init()                                   # Subsystem starten§\label{srcStart0003}§
    window = pygame.Window(size=(600, 400))         # Fenster erzeugen §\label{srcStart0005}§
    window.title = "Mein erstes Pygame-Programm"    # Fenstertitel §\label{srcStart0004}§
    window.position = (10, 50)                      # Fensterposition §\label{srcStart0002}§
    screen = window.get_surface()                   # Das Bitmap des Fensters holen §\label{srcStart0012}§

    running = True
    while running:                                  # Hauptprogammschleife: start §\label{srcStart0006}§
        for event in pygame.event.get():            # Ermitteln der Events§\label{srcStart0007}§
            if event.type == pygame.QUIT:           # Fenster X angeklickt? §\label{srcStart0008}§
                running = False
        screen.fill((0, 255, 0))                    # Spielfläche einfärben §\label{srcStart0009}§
        window.flip()                               # Doublebuffer austauschen §\label{srcStart0010}§

    pygame.quit()                                   # Subsystem beenden§\label{srcStart0011}§


if __name__ == "__main__":
    main()
