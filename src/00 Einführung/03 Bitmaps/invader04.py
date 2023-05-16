import os

import pygame


class Settings:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    FPS = 60
    ALIENS_NOF = 7


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Bitmaps laden und ausgeben")
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_pos_left = (Settings.WINDOW_WIDTH - 30) // 2       # linke Koordinate §\label{srcInvader0401}§
    defender_pos_top = Settings.WINDOW_HEIGHT - 30 - 5          # obere Koordinate §\label{srcInvader0402}§
    defender_pos = (defender_pos_left, defender_pos_top)        # Mache ein 2-Tupel §\label{srcInvader0403}§

    alien_image = pygame.image.load("images/alienbig0101.png").convert_alpha()
    alien_image = pygame.transform.scale(alien_image, (50, 45))
    space_for_aliens = Settings.ALIENS_NOF * 50                 # Verbrauchter Platz §\label{srcInvader0405}§
    space_availible = Settings.WINDOW_WIDTH - space_for_aliens  # Verfügbarer Platz §\label{srcInvader0406}§
    space_nof = Settings.ALIENS_NOF + 1                         # Anzahl Freiräume §\label{srcInvader0407}§
    space_between_aliens = space_availible // space_nof         # Platz Freiräume §\label{srcInvader0408}§

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        alien_top = 10                                          # Abstand von oben §\label{srcInvader0409}§
        for i in range(Settings.ALIENS_NOF):                    # Berechnung/Ausgabe§\label{srcInvader0410}§
            alien_left = space_between_aliens + i * (space_between_aliens + 50)
            alien_pos = (alien_left, alien_top)
            screen.blit(alien_image, alien_pos)
        screen.blit(defender_image, defender_pos)               # Benutze Position §\label{srcInvader0404}§
        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
